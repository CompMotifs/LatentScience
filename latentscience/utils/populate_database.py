import psycopg2
from psycopg2.extras import DictCursor
from sentence_transformers import SentenceTransformer
from latentscience.utils.csv_to_tuples import load_papers_data
from latentscience.config import Settings


# Embedding model from Hugging Face
MODEL_NAME = "all-MiniLM-L6-v2"  # Good balance of speed and quality

# --- 2. Sample Data ---
# A list of tuples: (title, abstract, field)
file_path = "../database_papers_links.csv"
load_papers_data(file_path)

# --- 3. Core Functions ---


def get_db_connection(settings: Settings):
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=settings.pg_host,
            dbname=settings.pg_database,
            user=settings.pg_user,
            password=settings.pg_password,
            port=settings.pg_port,
        )
        print("Database connection established successfully.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        print(
            "Please ensure the PostgreSQL container is running. Use 'docker-compose up -d'."
        )
        return None


def setup_database(conn):
    """Sets up the database by enabling pgvector and creating the papers table."""
    with conn.cursor() as cur:
        print("Enabling the 'vector' extension...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        print("Creating the 'papers' table if it does not exist...")
        # The vector size (384) must match the model's output dimension
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                abstract TEXT,
                field VARCHAR(100),
                embedding VECTOR(384)
            );
        """
        )
        conn.commit()
    print("Database setup complete.")


def generate_embeddings(model: SentenceTransformer, texts: list[str]):
    """Generates embeddings for a list of texts using the specified model."""
    print(f"Generating embeddings for {len(texts)} texts using '{MODEL_NAME}'...")
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings


def insert_data(conn, papers, embeddings) -> None:
    """Inserts paper data and their embeddings into the database."""
    print("Inserting data into the 'papers' table...")
    with conn.cursor() as cur:
        # Check if table is empty before inserting
        cur.execute("SELECT COUNT(*) FROM papers;")
        count = cur.fetchone()[0]
        if count > 0:
            print("Data already exists in the 'papers' table. Skipping insertion.")
            return

        for paper, embedding in zip(papers, embeddings):
            title, abstract, field = paper
            # Convert numpy array to list for psycopg2
            embedding_list = embedding.tolist()
            cur.execute(
                "INSERT INTO papers (title, abstract, field, embedding) VALUES (%s, %s, %s, %s)",
                (title, abstract, field, embedding_list),
            )
        conn.commit()
    print(f"{len(papers)} records inserted successfully.")


def perform_similarity_search(conn, model, query_text, top_k=3):
    """Performs a similarity search against the abstracts in the database."""
    print(f"\n--- Performing similarity search for query: '{query_text}' ---")

    # Generate embedding for the query text
    query_embedding = model.encode(query_text)
    query_embedding_list = query_embedding.tolist()

    with conn.cursor(cursor_factory=DictCursor) as cur:
        # Use the cosine distance operator (<=>) from pgvector
        cur.execute(
            """
            SELECT title, field, abstract, 1 - (embedding <=> %s) AS similarity
            FROM papers
            ORDER BY embedding <=> %s
            LIMIT %s;
        """,
            (query_embedding_list, query_embedding_list, top_k),
        )

        results = cur.fetchall()

    if not results:
        print("No results found.")
        return

    print(f"Top {top_k} most similar papers:")
    for row in results:
        print(f"\n  Title: {row['title']}")
        print(f"  Field: {row['field']}")
        print(f"  Similarity Score: {row['similarity']:.4f}")
        print(f"  Abstract: {row['abstract'][:150]}...")
