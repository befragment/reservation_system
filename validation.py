from typing import Final, Optional
from datetime import date, datetime

from pydantic import BaseModel, Field


_REGEX_PHONE_PATTERN: Final = r'^\+7\d{10}$'

class RentRequestBase(BaseModel):
    name: str
    phone_number: str = Field(pattern=_REGEX_PHONE_PATTERN)
    wished_date_start: date
    wished_date_end: date
    wishings: Optional[str]


class ContractBase(BaseModel):
    datetime_start: datetime
    datetime_end: datetime
    is_paid: bool = False
    request_id: int | None  # by default it goes to database with `null` value