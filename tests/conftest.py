import asyncio
from copy import deepcopy

import httpx
import pytest

from src import app as app_module


BASE_ACTIVITIES = deepcopy(app_module.activities)


class SyncASGIClient:
    def __init__(self, app):
        self._app = app

    def request(self, method, url, **kwargs):
        async def make_request():
            transport = httpx.ASGITransport(app=self._app)
            async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
                return await client.request(method, url, **kwargs)

        return asyncio.run(make_request())

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(deepcopy(BASE_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(deepcopy(BASE_ACTIVITIES))


@pytest.fixture()
def client():
    return SyncASGIClient(app_module.app)