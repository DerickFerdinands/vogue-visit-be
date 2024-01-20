from typing import Optional, List

from pydantic import BaseModel, Field


class AppointmentRQ(BaseModel):
    salon_id: int
    service_id: int
    slots: List[int]

