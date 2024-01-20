from typing import Optional

from pydantic import BaseModel, Field


class TimeSlotRq(BaseModel):
    date: str
    start_time: str
    end_time: str

