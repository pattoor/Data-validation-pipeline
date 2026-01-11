import pandas as pd
import numpy as np
from datetime import datetime

def generate_dirty_dataset():
    data = {
        "id": range(1, 11),
        "full_name": [
            "John Doe", "Jane Smith", "Invalid User", "Error 404", 
            None, "Corrupt Data", "Alice W.", "Bob M.", "Charlie B.", "Extra"
        ],
        "email": [
            "john@example.com", "jane@example.com", "bad-email.com", "test@@domain.com",
            "missing-at", "valid@test.io", None, "space in@email.com", "ok@ok.com", "last@one.com"
        ],
        "transaction_date": [
            "2023-01-01", "2023-02-30", "not-a-date", "2024-12-25",
            "2023/05/10", None, "2023-07-15", "2023-08-40", "2022-10-10", "2023-11-11"
        ],
        "amount": [
            150.50, -10.00, "100$", 0, 
            999.99, None, 50.00, 200.00, -500.00, 10.50
        ]
    }

    df = pd.DataFrame(data)
    
    # Crear carpeta si no existe
    import os
    os.makedirs('data/raw', exist_ok=True)
    
    df.to_csv('data/raw/dirty_data.csv', index=False)
    print("✅ Archivo 'data/raw/dirty_data.csv' generado con éxito.")

if __name__ == "__main__":
    generate_dirty_dataset()