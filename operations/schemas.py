from pydantic import BaseModel, Field
from typing import List


class Task(BaseModel):
    TITLE: str = Field(alias='title', max_length=50)
    DESCRIPTION: str = Field(alias='description')
    CREATED_BY: int = Field(alias='created_by')
    RESPONSIBLE_ID: int = Field(alias='responsible_id')
    AUDITORS: List[int] = Field(alias='auditors')
