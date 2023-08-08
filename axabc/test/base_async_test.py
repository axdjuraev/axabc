import pytest
from asyncio import new_event_loop, set_event_loop


loop = new_event_loop()


class BaseAsyncTest:
    @pytest.fixture(scope='session')
    def event_loop(self):
        set_event_loop(loop)
        yield loop