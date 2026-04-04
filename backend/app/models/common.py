from pydantic import BaseModel, ConfigDict


class APIResponse(BaseModel):
    success: bool = True
    message: str


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int


class PaginatedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool = True
    message: str
    meta: PaginationMeta
    items: list

