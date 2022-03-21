from typing import Optional, Generic, TypeVar, Any

from pydantic import BaseModel
import sqlalchemy.engine
import sqlalchemy.engine.interfaces
import sqlalchemy.event
import sqlalchemy.orm
import sqlparse


def page(
    query: "sqlalchemy.orm.Query[Any]", skip: int, limit: int
) -> "sqlalchemy.orm.Query[Any]":
    """Paginate a `Query`

    Kwargs:
        per_page (str): Number of rows per page
        page (str): Page number to display

    Returns
        query (sqlalchemy.orm.Query): The paginated query
    """
    return query.limit(limit).offset(skip)


T = TypeVar("T")


class Paged(BaseModel, Generic[T]):
    """Page a model result set"""

    total: int
    results: list[T]
    skip: Optional[int]
    limit: Optional[int]

    @property
    def first(self) -> T:
        return self.results[0]


def pretty(query: "sqlalchemy.orm.Query[Any]", show: bool = False) -> str:
    """Pretty print a `Query`"""
    text: str = sqlparse.format(str(query), reindent=True, keyword_case="upper")
    if show:
        print(text)

    return text


def with_metadata(
    results: list[sqlalchemy.engine.row.Row], metadata: list[str]
) -> list[sqlalchemy.engine.row.Row]:
    """Add metadata to rows base _metadata attribute"""
    # breakpoint()

    parsed = []
    for result in results:
        for meta_id, meta_value in enumerate(result[1:]):
            result[0]._metadata[metadata[meta_id]] = meta_value
        parsed.append(result[0])

    return parsed


class CustomBase:
    @property
    def _metadata(self) -> dict[str, Any]:
        if not hasattr(self, "_additional_metadata"):
            self._additional_metadata: dict[str, Any] = {}
        return self._additional_metadata
