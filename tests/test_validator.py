import pytest 
from pydantic import ValidationError
from src.models import TransactionModel

# 1. Valid Data Test (Happy Path)
def test_valid_transaction():
    """Tests a perfect data scenario to ensure the model accepts correct data."""
    valid_data = {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com",
        "transaction_date": "2023-01-01",
        "amount": 150.50
    }
    # If it does not raise an exception, the test passes
    instance = TransactionModel(**valid_data)
    assert instance.full_name == "John Doe"
    assert instance.id == 1
    assert instance.transaction_date.year == 2023
    
# Negative tests (Error Path)
# 2. Invalid email test
def test_invalid_email_raises_validation_error():
    """Malformed email must raise a ValidationError from EmailStr."""
    data = {"id": 2, 
            "full_name": "Jane Doe", 
            "email": "not-an-email", 
            "transaction_date": "2023-01-01", 
            "amount": 100.0
        }
    # pydantic's EmailStr error contains 'value is not a valid email address'
    with pytest.raises(ValidationError, match=r"value is not a valid email address"):
        TransactionModel(**data)

# 3. Negative amount test
def test_negative_amount_raises_validation_error():
    """Amount must be greater than 0 (Field(gt=0))."""
    data = {"id": 3, 
            "full_name": "Jane Doe", 
            "email": "jane@example.com", 
            "transaction_date": "2023-01-01", 
            "amount": -50.0
        }
    # Match either default pydantic message or possible custom phrasing
    with pytest.raises(ValidationError, match=r"greater than 0|ensure this value is greater than 0"):
        TransactionModel(**data)

# 4. Invalid date format test
def test_invalid_date_format_raises_value_error():
    """Invalid date strings must raise our custom ValueError from parse_date."""
    data = {"id": 4, 
            "full_name": "Jane Doe", 
            "email": "jane@example.com", 
            "transaction_date": "2023-13-45", 
            "amount": 10.0
        }
    with pytest.raises(ValueError, match=r"Invalid date format"):
        TransactionModel(**data)

# 5. Corrupt name keyword test
def test_corrupt_name_keyword_rejected():
    """Custom validator rejects names containing junk keywords."""
    data = {"id": 5, 
            "full_name": "Corrupt Data Row", 
            "email": "test@test.com", 
            "transaction_date": "2023-01-01", 
            "amount": 10.0
        }
    with pytest.raises(ValueError, match=r"Name contains invalid keywords"):
        TransactionModel(**data)

# 6. Missing required field test
def test_missing_required_field_raises():
    """Missing mandatory fields should raise ValidationError (field required)."""
    data = {"id": 6, 
            "full_name": "No Email User", 
            "transaction_date": "2023-01-01", 
            "amount": 100.0
        }
    with pytest.raises(ValidationError, match=r"field required|Field required"):
        TransactionModel(**data)

# 7. Boundary test for amount = 0
def test_amount_zero_fails_boundary():
    """Zero amount should fail when gt=0 is enforced."""
    data = {"id": 7, 
            "full_name": "Zero User", 
            "email": "zero@test.com", 
            "transaction_date": "2023-01-01", 
            "amount": 0.0
        }
    with pytest.raises(ValidationError, match=r"greater than 0|ensure this value is greater than 0"):
        TransactionModel(**data)

# 8. Whitespace name test
def test_whitespace_name_fails_min_length():
    """Names with only whitespace violate min_length constraint."""
    data = {
        "id": 8, 
        "full_name": "   ", 
        "email": "space@test.com", 
        "transaction_date": "2023-01-01", 
        "amount": 10.0
        }
    # pydantic error message for min_length varies; match generic 'at least' phrase
    with pytest.raises(ValidationError, match=r"at least|at least 3|ensure this value has at least"):
        TransactionModel(**data)

# 9. Wrong data types test
def test_wrong_data_types_raise_validation_error():
    """Type mismatches (id as string, amount as non-numeric) should raise ValidationError."""
    data = {"id": 
        "not-a-number", 
        "full_name": 12345, 
        "email": "test@test.com", 
        "transaction_date": "2023-01-01", 
        "amount": "Cien dolares"
        }
    with pytest.raises(ValidationError, match=r"value is not a valid|Input should be a valid|invalid"):
        TransactionModel(**data)

# 10. Future date test
def test_future_date_parsed_correctly():
    """A far future date in correct format should be parsed and accessible."""
    data = {"id": 10, 
            "full_name": "Future Man", 
            "email": "future@test.com", 
            "transaction_date": "2099-12-31", 
            "amount": 500.0
        }
    instance = TransactionModel(**data)
    assert instance.transaction_date.year == 2099
