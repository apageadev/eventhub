# eventhub

[![codecov](https://codecov.io/gh/apageadev/eventhub/graph/badge.svg?token=IEKZKP7ER6)](https://codecov.io/gh/apageadev/eventhub)

`EventHub` provides a lightweight event management system for Python projects using a simple publish/subscribe pattern.

## Installation

```bash
pip install eventhub
```

**NOTE**: This example requires `redis` or a `redis` compatible server (like [DragonflyDB](https://github.com/dragonflydb/dragonfly])) to be running on `localhost:6379`.

## Usage Example

For a simple example, consider the following code:

`pub.py`:

```python
import uuid
import asyncio
from eventhub import EventHub, Event

from redis.asyncio import Redis

r = Redis(host='localhost', port=6379, db=0)

# PUBLISH/SUBSCRIBE example (one-way communication)
async def main():
    hub = EventHub(r)

    for i in range(10):
        # for every other event, publish to a different topic
        if i % 2 == 0:
            event = Event(topic="foo", payload={"id": str(uuid.uuid4())})
        else:
            event = Event(topic="bar", payload={"id": str(uuid.uuid4())})

        await hub.publish(event)


    await hub.close()


if __name__ == "__main__":
    asyncio.run(main())
```

`sub.py`:

```python
import asyncio
from eventhub import EventHub, Event
from redis.asyncio import Redis

r = Redis(host='localhost', port=6379, db=0)

hub = EventHub(r)

@hub.subscribe(topic="foo")
async def handler_foo(event: Event):
    print("got foo event", event)

@hub.subscribe(topic="foo")
async def handler_foo2(event: Event):
    print("got foo event (2)", event)

@hub.subscribe(topic="bar")
async def handler_bar(event: Event):
    print("got bar event", event)

async def main():
    await hub.start()

async def shutdown():
    print("Shutting down EventHub...")
    await hub.shutdown()
    print("EventHub shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Instead of directly running hub.shutdown() in another asyncio.run,
        # we ensure that the shutdown process completes before closing the loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(shutdown())
        loop.close()
```

example output:

```
got foo event topic='foo' payload={'id': '44f22b8b-0cef-427f-9bbe-2e6b4d43803a'}
got foo event (2) topic='foo' payload={'id': '44f22b8b-0cef-427f-9bbe-2e6b4d43803a'}
got bar event topic='bar' payload={'id': '9c8ec0bd-209b-40cb-bc04-66ee6bd4c82c'}
got foo event topic='foo' payload={'id': '8684450c-1382-46ba-8559-1a3791491973'}
got foo event (2) topic='foo' payload={'id': '8684450c-1382-46ba-8559-1a3791491973'}
got bar event topic='bar' payload={'id': 'be887cd5-bd35-4587-a138-b85c10a68fab'}
got foo event topic='foo' payload={'id': '619a9d16-99b1-46a2-9108-7fa114c03d8c'}
got foo event (2) topic='foo' payload={'id': '619a9d16-99b1-46a2-9108-7fa114c03d8c'}
got bar event topic='bar' payload={'id': 'e1ffeb07-073d-42a5-af1f-8c3032d053b9'}
got foo event topic='foo' payload={'id': '6124ecd0-e7e0-4754-bbef-43b6f6a610d2'}
got foo event (2) topic='foo' payload={'id': '6124ecd0-e7e0-4754-bbef-43b6f6a610d2'}
got bar event topic='bar' payload={'id': '80b2e02e-b8d4-4f9b-8821-089a69dcdf9c'}
got foo event topic='foo' payload={'id': 'c0ddd161-9a14-4c4d-9369-2948cb75eec9'}
got foo event (2) topic='foo' payload={'id': 'c0ddd161-9a14-4c4d-9369-2948cb75eec9'}
got bar event topic='bar' payload={'id': '8904d68e-9213-4376-92c5-d05fc438410a'}
```
