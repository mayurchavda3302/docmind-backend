import pydantic


class RAGChunkAndSrc(pydantic.BaseModel):
    chunks: list[str]
    sourc_id: str = None


class RAGUpsertResult(pydantic.BaseModel):
    ingested: int


class RAGSearchResult(pydantic.BaseModel):
    contexts: list[str]
    sources: list[str]


class RAGQuaryResult(pydantic.BaseModel):
    answer: str
    sources: list[str]
    number_context: int
