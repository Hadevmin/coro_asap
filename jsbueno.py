import asyncio
from heapq import heappush, heapify
import aiohttp


class PriorityGroups:
    def __init__(self):
        self.priority_queue = []
        self.counter = 0

    async def sleep(self, priority=10):
        counter = self.counter
        self.counter += 1
        steps = .001  # granularity
        step = 0
        heappush(self.priority_queue, (priority, counter))
        try:
            while step < steps or (self.priority_queue and self.priority_queue[0][0] < priority):
                await asyncio.sleep(0)
                step += 1
        finally:
            self.priority_queue.remove((priority, counter))
            heapify(self.priority_queue)


priority_group = PriorityGroups()


async def another_coro(i, session, priority=1):
    await priority_group.sleep(priority)
    print(i)  # to observe the order of execution
    # HTTP request
    async with session.request(method='GET', url=f'/Hadevmin/coro_asap/blob/main/{i}') as resp:
        await resp.text()


async def coro(i, session):
    if i == 1:
        async with asyncio.TaskGroup() as tg_fast:
            tg_fast.create_task(another_coro(i * 10, session))
            tg_fast.create_task(another_coro(i * 100, session))
    else:
        await priority_group.sleep()
        print(i)  # to observe the order of execution
        # HTTP request
        async with session.request(method='GET', url=f'/Hadevmin/coro_asap/blob/main/{i}') as resp:
            await resp.text()


async def main():
    session = aiohttp.ClientSession('https://github.com')
    async with asyncio.TaskGroup() as tg_main:
        for i in range(0, 3):
            tg_main.create_task(coro(i, session))
    await session.close()


asyncio.run(main(), debug=True)
