from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ReportQuery(BaseModel):
    report_id: str = Field(alias='id')
    report_name: str = Field(alias='name')
    report_date: datetime = Field(alias='createDate')
    timeout: int = Field(alias='timeoutSecs')
    pg_id: int = Field(alias='productGroupCode')
    inn: str = Field(alias='orgInn')
    status_id: str = Field(alias='currentStatus')
    cis_status: str = ''

    @field_validator('status_id')
    def set_status(cls, s: str) -> int:
        match s:
            case "PREPARATION":
                return 1


class ReportQueryResponse(BaseModel):
    report_id: str = Field(alias='id')
    report_name: str = Field(alias='name')
    inn: str = Field(alias='orgInn')
    status_id: str = Field(alias='currentStatus')
    status_date: datetime = datetime.now()

    @field_validator('status_id')
    def set_status(cls, s: str) -> int:
        match s:
            case "PREPARATION":
                return 1
            case "COMPLETED":
                return 2
            case "CANCELED":
                return 3
            case "ARCHIVE":
                return 4
            case "FAILED":
                return 5

class ReportQueryIdToDownload(BaseModel):
    file_id: str = Field(alias='id')
    report_id: str = Field(alias='taskId')
    available_to_download: str = Field(alias='available')
    download_status: str = Field(alias='downloadStatus')
    status_date: datetime = datetime.now()
