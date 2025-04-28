from pydantic import BaseModel, Field


class Person(BaseModel):
    first: str = Field(..., description="The person's first name.")
    last: str = Field(..., description="The person's last name.")
    age: int | None = Field(
        None, description="Age in years which must be equal to or greater than zero."
    )
