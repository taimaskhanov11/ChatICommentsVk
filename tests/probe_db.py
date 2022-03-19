import asyncio

import aioredis

redis = aioredis.from_url("redis://localhost",decode_responses=True)


async def main():
    # await redis.incr("my-key")
    # value = await redis.get("my-key")
    value = await redis.getset("qwer", 1)
    print(value)
    # await redis.flushall()


if __name__ == "__main__":
    asyncio.run(main())
