from pydantic import BaseModel, EmailStr, Field, field_validator, StringConstraints
from datetime import datetime
from typing import Optional, Annotated

# Define a Pydantic model to validate the dataset. The Data Contract

class TransactionModel(BaseModel):
    # Field validation examples
    id: int
    full_name: Annotated[ 
        str, 
        StringConstraints(min_length=3, strip_whitespace=True)
    ] 
    email: EmailStr  # Validates email format automatically
    transaction_date: datetime
    amount: float = Field(gt=0) # Must be greater than 0

    @field_validator("full_name") # Custom validator for full_name
    @classmethod
    def name_must_not_be_junk(cls, v: str) -> str:
        # Custom logic to reject names that look like errors
        if "Error" in v or "Corrupt" in v:
            raise ValueError("Name contains invalid keywords (Error/Corrupt)")
        return v

    @field_validator("transaction_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        # Handle cases where dates might be in different formats or null
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format: {v}. Expected YYYY-MM-DD")
        return v