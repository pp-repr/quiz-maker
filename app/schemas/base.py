from pydantic import BaseModel
from typing import Type, Any, TypeVar

T = TypeVar('T', bound='BaseRequest')


class BaseRequest(BaseModel):
    @classmethod
    def form(cls: Type[T], **form_data: Any) -> T:
        return cls(**form_data)