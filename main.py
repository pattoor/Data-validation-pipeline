from src.validator import process_data

if __name__ == "__main__":
    print("🚀 Starting Data Validation Pipeline...")
    
    input_file = 'data/raw/dirty_data.csv'
    
    clean_count, error_count = process_data(input_file)
    
    print("-" * 30)
    print(f"✅ Processing Complete!")
    print(f"📂 Clean records saved: {clean_count}")
    print(f"❌ Corrupt records identified: {error_count}")
    print(f"📝 Check 'data/reports/Validation_Errors.json' for details.")