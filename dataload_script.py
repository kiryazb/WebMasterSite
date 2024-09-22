import asyncio
import contextlib
from typing import Tuple
from db.session import connect_db
from api.config.models import YandexLr
from api.auth.schemas import UserCreate
from api.config.models import Role
from api.auth.manager import get_user_manager
from api.auth.utils import get_user_db


DB_NAME = 'general'


async def add_test_role(id: int, name: str) -> None:
    """
    Adds new role
    """
    try:
        async_session = await connect_db(DB_NAME)
        async with async_session() as session:
            new_role = Role(id=id, name=name)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
        print("\033[92m'{}\033[00m".format(f"{name}' role is added"))
    except Exception as e:
        print("\033[91m{}\033[00m".format(f"New role is not created due to the following error: {e}"))


async def add_test_user(id: int, email: str, username: str, role: str, password: str) -> None:
    """
    Adds new user
    """
    try:
        async_session = await connect_db(DB_NAME)
        get_user_db_context = contextlib.asynccontextmanager(get_user_db)
        get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
        async with async_session() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    new_user = await user_manager.create(
                        UserCreate(
                            id=id, email=email, username=username, password=password
                        )
                    )
                    new_user.role = role
                    session.add(new_user)
                    await session.commit()
    except Exception as e:
        print("\033[91m{}\033[00m".format(f"New user is not created due to the following error: {repr(e)}"))


async def add_new_regions(regions_list: Tuple[Tuple[int, str, int], ...]) -> None:
    """
    Adds new regions
    """
    try:
        async_session = await connect_db(DB_NAME)
        async with async_session() as session:
            new_regions = [YandexLr(id=id, Geo=name, Geoid=geoid) for id, name, geoid in regions_list]
            session.add_all(new_regions)
            await session.commit()
        if len(regions_list) > 1:
            print("\033[92m{}\033[00m".format(f"{', '.join([region[1] for region in regions_list])} regions are added"))
        else:
            print("\033[92m{}\033[00m".format(f"{regions_list[0][1]}' region is added"))
    except Exception as e:
        print("\033[91m{}\033[00m".format(f"New geo is not created due to the following error: {e}"))


async def main():
    await asyncio.gather(
        add_test_role(4, 'Search'),
        add_test_user(1, "testuser@gmail.com", 'testuser', 4,
                      "testpassword"),
        add_new_regions(((1, 'Москва', 77), (2, 'Санкт-Петербург', 78)))
    )

if __name__ == "__main__":
    asyncio.run(main())
