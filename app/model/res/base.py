
from typing import Any, Dict, Type
from pydantic import BaseModel, Field


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return str(v)
        except ValueError:
            raise ValueError


class BaseRes(BaseModel):
    id: OID = Field(alias="_id")

    class Config:
        
        # remove underline in "_id" variable name which show on swagger response schema
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type['BaseRes']) -> None:
            new_schema = {}
            for k in schema.get('properties').keys():
                v=schema.get('properties').get(k)
                if(k.startswith("_")):
                    k = k[1:]
                new_schema.update({k: v})
            
            schema.update({'properties': new_schema})
