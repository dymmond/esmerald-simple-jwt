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


@pytest.fixture(autouse=True, scope="module")
async def create_test_database():
    try:
        await models.create_all()
        yield
        await models.drop_all()
    except Exception:
        pytest.skip("No database available")


@pytest.fixture(autouse=True)
async def rollback_transactions():
    with database.force_rollback():
        async with database:
            yield
