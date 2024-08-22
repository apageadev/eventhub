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