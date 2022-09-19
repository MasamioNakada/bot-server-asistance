from re import M
from pydantic import BaseModel, Field

class User(BaseModel):
    user_id : str = Field(
        ...,
        min_length=1,
        max_length=20,
        example='51952841852@.se'
    )
    message : str = Field(
        ...,
        example='/proceso de seleccion'
    )
