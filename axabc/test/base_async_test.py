import pytest
from asyncio import new_event_loop


class BaseAsyncTest:
    @pytest.fixture()
    def event_loop(self):
        loop = new_event_loop()
        yield loop
        loop.close()

