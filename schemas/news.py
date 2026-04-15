from pydantic import BaseModel, Field


class News(BaseModel):
    """Model for representing news from the PPGEEC website"""

    title: str = Field("", description="Title of the news article")
    id: int = Field(0, description="ID of the news article")
    url: str = Field("", description="URL of the news article")


__all__ = ["News"]
