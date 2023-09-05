from pydantic import BaseModel, Field, validator, UUID4
from typing import List, Optional
from datetime import date
import json

class Person(BaseModel):
    apelido: str = Field(..., max_length=32)
    nome: str = Field(..., max_length=100)
    nascimento: date
    stack: Optional[List[str]]
        
class PersonResponse(Person):
    id: UUID4
        
    @classmethod
    def from_db(cls, id, apelido, nome, nascimento, stack):
        return cls(
            id=id,
            apelido=apelido,
            nome=nome,
            nascimento=nascimento,
            stack=json.loads(stack) if stack else None
        )