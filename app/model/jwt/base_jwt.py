# abc rely on nominal typing, the relationship must explicitly announce(like inheritence)
# protocol rely on structural typing, is the structure the same(same method, properties)? if yes, program works

from typing import Protocol


class BaseJwt(Protocol):
    def extract_email(self)->str:
        ...