from datetime import datetime

from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]

external_data = {'id': 'not an int', 'tastes': {}}

try:
    User(**external_data)
except ValidationError as e:
    print(e.errors())