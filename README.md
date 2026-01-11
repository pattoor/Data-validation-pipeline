# Data Quality & Validation Pipeline

## 🚀 Overview
A robust Python-based ETL pipeline designed to enforce **Data Quality** standards. This project demonstrates how to handle "dirty" datasets by using **Pandas** for data processing and **Pydantic** for schema enforcement and business rule validation.

## 🛠 Tech Stack
- **Python 3.10+**
- **Pandas**: High-performance data manipulation.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Pytest**: Professional testing framework.
- **GitHub Actions**: CI/CD for automated quality checks.

## 📁 Project Structure
- `src/`: Core logic and Pydantic models.
- `data/`: Raw, processed, and error report storage.
- `tests/`: Unit tests for data integrity.
- `.github/`: CI configuration.

## 🔧 Installation & Usage
1. Clone the repo: `git clone https://github.com/pattoor/Data-validation-pipeline.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the generator: `python generate_raw_data.py`
4. Execute the pipeline: `python main.py`
5. Run tests: `pytest -v`

## 📊 Features
- **Automated Validation**: Identifies missing values, wrong formats, and out-of-range numbers.
- **Error Reporting**: Generates a detailed `Validation_Errors.json` for data auditing.
- **CI/CD Integration**: Automated testing on every push.