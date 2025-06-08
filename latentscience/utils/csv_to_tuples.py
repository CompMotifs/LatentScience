# Convert a CSV file with paper data into a list of tuples for further processing.
import pandas as pd

def load_papers_data(file_path):
    # Load the original CSV
    df = pd.read_csv(file_path)
    df.dropna(how='all',inplace=True)

    # Create two separate DataFrames: one for source, one for target
    source_df = df[["Source Domain", "Source Paper Title", "Source Abstract"]].copy()
    source_df.columns = ["domain", "paper_title", "abstract"]
    target_df = df[["Target Domain", "Target Paper Title", "Target Abstract"]].copy()
    target_df.columns = ["domain", "paper_title", "abstract"]

    # Concatenate source and target into a single DataFrame
    combined_df = pd.concat([source_df, target_df], ignore_index=True)
    # Drop any rows with missing abstracts (optional)
    combined_df.dropna(subset=["abstract"], inplace=True)
    # Reset index
    combined_df.reset_index(drop=True, inplace=True)

    PAPERS_DATA = list(combined_df.itertuples(index=False, name=None))
    # abstracts = [paper[2] for paper in PAPERS_DATA]
    return PAPERS_DATA

file_path = "../database_papers_links.csv"
load_papers_data(file_path)
