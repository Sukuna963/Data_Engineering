from pydantic import BaseModel

# Structure of the `get_trends`
class TrendItem(BaseModel):
    name: str
    url: str