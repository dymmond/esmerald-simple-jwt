import pytest
from esmerald.conf import settings

database, models = settings.edgy_registry


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
