import pytest
from redis.asyncio import Redis
from unittest.mock import AsyncMock
from eventhub import EventHub, Event

r = Redis(host="localhost", port=6379, db=0)


@pytest.mark.asyncio
async def test_eventhub_connection():
    """
    test EventHub connection
    """
    hub = EventHub(r)
    try:
        assert await hub.ping()
    finally:
        await hub.close()  # Close the connection using the close method


@pytest.mark.asyncio
async def test_eventhub_publish():
    """
    test EventHub publish
    """
    hub = EventHub(r)
    try:
        event = Event(topic="test", payload={"foo": "bar"})
        await hub.publish(event)
    finally:
        await hub.close()
