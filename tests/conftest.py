import os

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite:///test_comunidade.db"

import pytest  # noqa: E402

from fakepinterest import app, database  # noqa: E402


@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with app.app_context():
        database.drop_all()
        database.create_all()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        database.drop_all()
