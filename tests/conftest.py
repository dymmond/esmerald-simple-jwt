import pytest
from esmerald import Esmerald, Include
from esmerald.conf import settings
from esmerald.testclient import EsmeraldTestClient

database, models = settings.edgy_registry


def create_app():
    app = Esmerald(routes=[Include(path="/simple-jwt", namespace="esmerald_simple_jwt.urls")])
    return app


def get_client():
    return EsmeraldTestClient(create_app())


@pytest.fixture(scope="module")
def anyio_backend():
    return ("asyncio", {"debug": False})


@pytest.fixture
def app():
    return create_app()


@pytest.fixture(autouse=True, scope="function")
async def create_test_database():
    try:
        async with database:
            await models.create_all()
            yield
            if not database.drop:
                await models.drop_all()
    except Exception:
        pytest.skip("No database available")


@pytest.fixture(autouse=True)
async def rollback_transactions():
    async with models.database:
        yield
