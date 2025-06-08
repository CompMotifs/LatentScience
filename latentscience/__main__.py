import argparse
import os
import sys

from sentence_transformers import SentenceTransformer
import uvicorn

from latentscience.api.app import create_app
from latentscience.config import get_settings
from latentscience.utils.populate_database import (
    get_db_connection,
    setup_database,
    generate_embeddings,
    insert_data,
    PAPERS_DATA,
    MODEL_NAME,
)


def populate_database():
    """Populate the database with sample papers and embeddings."""

    print("Populating database...")
    settings = get_settings()

    # Establish database connection
    conn = get_db_connection(settings)
    if not conn:
        print("Failed to connect to database")
        sys.exit(1)

    # Load the embedding model
    print("Loading sentence-transformer model...")
    model = SentenceTransformer(MODEL_NAME)

    # Set up the database schema
    setup_database(conn)

    # Prepare data and generate embeddings
    abstracts = [paper[1] for paper in PAPERS_DATA]
    embeddings = generate_embeddings(model, abstracts)

    # Insert data into the database
    insert_data(conn, PAPERS_DATA, embeddings)

    # Close the database connection
    conn.close()
    print("Database population complete.")


def start_api():
    """Start the API server."""
    app = create_app()

    print("Starting API...")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=debug,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LatentScience application")
    parser.add_argument(
        "--populate", action="store_true", help="Populate the database with sample data"
    )
    parser.add_argument("--api", action="store_true", help="Start the API server")

    args = parser.parse_args()

    if args.populate:
        populate_database()
    elif args.api:
        start_api()
    else:
        # Default behavior - start API
        start_api()
