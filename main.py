import asyncio
from typing import Any, Coroutine, List, Type, Union

from pydantic import BaseModel

from db import AbstractAsyncRepository, AbstractAsyncUOW, BaseRepoCollector, TRepo


class User(BaseModel):
    ...


class Repo(AbstractAsyncRepository):
    IModel = User

    async def get(self, *identifiers: List[Any]) -> Any:
        return "hellow world"

    async def add(self, obj: IModel) -> IModel:
        return self.IModel()


class RepoCollection(BaseRepoCollector):
    user: Repo


class SQLAlchemyUOW(AbstractAsyncUOW):
    def __init__(self) -> None:
        self.repo = RepoCollection(_uow=self)

    def get_repo(self, repo_cls: Type[TRepo]) -> TRepo:
        return repo_cls(None)


async def _main():
    uow = SQLAlchemyUOW()
    val = await uow.repo.user.add(User())
    print(val)


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()
