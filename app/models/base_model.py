from datetime import datetime
from sqlmodel import SQLModel, Field
import pytz

def get_default_datetime()->datetime:
    utc_now = datetime.now(pytz.utc)
    ho_chi_minh_now = utc_now.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
    naive_now = ho_chi_minh_now.replace(tzinfo=None)
    return naive_now

class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=get_default_datetime,
        nullable=True,
    )



