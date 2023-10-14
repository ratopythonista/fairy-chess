import re


from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    summoner_name: str = Field('', description="User summoner name")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.fullmatch(regex, email):
            return email
        raise ValueError("Invalid email")    
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        regex = r'[\d|\w|]{8,}'
        if re.fullmatch(regex, password):
            return password
        raise ValueError("Invalid password")

class RiotUser(BaseModel):
    summoner_name: str = Field(..., description="User summoner name")
    icon: str = Field(..., description="URL for user icon")
    rank: str = Field(..., description="User Ranking")
    rank_icon: str = Field(..., description="User Ranking Icon")
    