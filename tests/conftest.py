import pytest
from esmerald import Esmerald, Include
from esmerald.conf import settings
from esmerald.testclient import EsmeraldTestClient

database, models = settings.edgy_registry


def create_app():
    from edgy import Instance, monkay

    # ensure the settings are loaded
    monkay.evaluate_settings(
        ignore_preload_import_errors=False,
        onetime=False,
    )
    app = Esmerald(routes=[Include(path="/simple-jwt", namespace="esmerald_simple_jwt.urls")])
    monkay.set_instance(Instance(registry=app.settings.registry, app=app))
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
    async with models.database:
        await models.create_all()
        yield
        if not models.database.drop:
            await models.drop_all()


@pytest.fixture(autouse=True, scope="function")
async def rollback_transactions():
    async with models.database:
        yield
