import asyncio


async def coro_a():
    print("I am coro_a(). Hi!")

async def coro_b():
    print("I am coro_b(). I sure hope no one hogs the event loop...")

async def main():
    task_b = asyncio.create_task(coro_b())
    num_repeats = 3
    for _ in range(num_repeats):
        await coro_a()
    await task_b


async def main_2():
    task_b = asyncio.create_task(coro_b())
    num_repeats = 3
    for _ in range(num_repeats):
        await asyncio.create_task(coro_a())
    await task_b


asyncio.run(main())
print("---------------------------------------------------------------")
asyncio.run(main_2())