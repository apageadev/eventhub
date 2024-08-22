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
