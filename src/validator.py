import pandas as pd
import json
import os
from src.models import TransactionModel
from pydantic import ValidationError

# The Processing Engine. read and filter the data based on the Data Contract
def process_data(input_path: str):
    # Ensure output directories exist
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/reports', exist_ok=True)

    df = pd.read_csv(input_path)
    clean_rows = []
    error_logs = []

    # Iterate through the dataframe rows
    for index, row in df.iterrows():
        try:
            # Convert row to dictionary and drop NaN values for Pydantic validation
            row_dict = row.to_dict()
            # Clean NaN/None to avoid Pydantic issues with optional fields
            row_dict = {k: v for k, v in row_dict.items() if pd.notna(v)}
            
            # Validate row against the model
            validated_row = TransactionModel(**row_dict)
            clean_rows.append(validated_row.model_dump())
            
        except (ValidationError, ValueError) as e:
            # Capture the error details and the row index
            error_logs.append({
                "row_index": index + 2, # +2 to match CSV line number (1-based + header)
                "errors": json.loads(e.json()) if hasattr(e, 'json') else str(e),
                "original_data": row.to_dict()
            })

    # Save Clean Data
    clean_df = pd.DataFrame(clean_rows)
    clean_df.to_csv('data/processed/Clean_Data.csv', index=False)

    # Save Error Report
    with open('data/reports/Validation_Errors.json', 'w') as f:
        json.dump(error_logs, f, indent=4)

    return len(clean_rows), len(error_logs)