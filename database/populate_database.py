# # in terminal
# python -m venv myenv
# myenv\Scripts\activate
# pip install numpy pandas matplotlib

# pip install sentence-transformers 
# pip install psycopg2-binary pgvector

# docker-compose up -d 
# python populate_database.py

# populate_database.py
import psycopg2
from psycopg2.extras import DictCursor
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# --- 1. Configuration ---
# Database connection details
DB_HOST = "localhost"
DB_NAME = "ai_papers"
DB_USER = "user"
DB_PASSWORD = "password"
DB_PORT = "5432"

# Embedding model from Hugging Face
MODEL_NAME = 'all-MiniLM-L6-v2' # Good balance of speed and quality

# --- 2. Sample Data ---
# A list of tuples: (title, abstract, field)
# TODO: load from a file
PAPERS_DATA = [
    (
        "Mapping Brain Circuits with High-Resolution Connectomics",
        "Recent advances in electron microscopy and computational analysis allow for the dense reconstruction of neural circuits. We mapped a cubic millimeter of mouse visual cortex, revealing novel synaptic motifs and cell type-specific connectivity patterns that challenge existing models of cortical processing.",
        "Neuroscience"
    ),
    (
        "A Programmable DNA-Based Platform for Engineering Synthetic Gene Circuits",
        "We have developed a robust and scalable framework for designing synthetic gene circuits using programmable DNA components. This platform enables the construction of complex logical functions within living cells, paving the way for advanced diagnostics and therapeutics.",
        "Synthetic Biology"
    ),
    (
        "The Role of Astrocytes in Synaptic Plasticity and Memory",
        "Beyond their supportive role, astrocytes are active participants in synaptic function. Our findings demonstrate that astrocytes modulate synaptic plasticity through gliotransmitter release, a mechanism crucial for learning and memory formation in the hippocampus.",
        "Neuroscience"
    ),
    (
        "Self-Assembling Protein Nanomaterials for Targeted Drug Delivery",
        "This work describes the design and synthesis of protein-based nanomaterials that self-assemble into well-defined structures. By functionalizing these materials with targeting ligands, we achieved highly specific delivery of chemotherapeutic agents to cancer cells, minimizing off-target toxicity.",
        "Synthetic Biology"
    ),
    (
        "Decoding Neural Representations of Visual Objects",
        "Using functional magnetic resonance imaging (fMRI) and machine learning, we investigated how the human brain represents visual objects. We found that object categories are encoded in distributed and overlapping patterns of neural activity across the ventral temporal cortex, providing insights into the brain's organizational principles.",
        "Neuroscience"
    )
]

# --- 3. Core Functions ---

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Database connection established successfully.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        print("Please ensure the PostgreSQL container is running. Use 'docker-compose up -d'.")
        return None

def setup_database(conn):
    """Sets up the database by enabling pgvector and creating the papers table."""
    with conn.cursor() as cur:
        print("Enabling the 'vector' extension...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        print("Creating the 'papers' table if it does not exist...")
        # The vector size (384) must match the model's output dimension
        cur.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                abstract TEXT,
                field VARCHAR(100),
                embedding VECTOR(384)
            );
        """)
        conn.commit()
    print("Database setup complete.")

def generate_embeddings(model, texts):
    """Generates embeddings for a list of texts using the specified model."""
    print(f"Generating embeddings for {len(texts)} texts using '{MODEL_NAME}'...")
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

def insert_data(conn, papers, embeddings):
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
                (title, abstract, field, embedding_list)
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
        cur.execute("""
            SELECT title, field, abstract, 1 - (embedding <=> %s) AS similarity
            FROM papers
            ORDER BY embedding <=> %s
            LIMIT %s;
        """, (query_embedding_list, query_embedding_list, top_k))
        
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

# --- 4. Main Execution Block ---

if __name__ == "__main__":
    
    # Establish database connection
    conn = get_db_connection()
    
    # Load the embedding model
    print("Loading sentence-transformer model...")
    model = SentenceTransformer(MODEL_NAME)

    if conn:
        # Set up the database schema
        setup_database(conn)

        # Prepare data and generate embeddings
        abstracts = [paper[1] for paper in PAPERS_DATA]
        embeddings = generate_embeddings(model, abstracts)

        # Insert data into the database
        insert_data(conn, PAPERS_DATA, embeddings)

        # Perform a sample search
        search_query = "brain connectivity"
        perform_similarity_search(conn, model, search_query)
        
        # Close the database connection
        conn.close()
        print("\nDatabase connection closed.")
