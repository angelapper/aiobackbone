# coding=utf-8

"""App Start up
Author: Angelapper
Python Version: 3.6

Changes:
--------
1. using aiohttp launch app with logging

"""
import argparse
import logging.config
import asyncio
import aiohttp
from aiohttp import web
import uvloop
import ujson
import sys
import os
from .settings import settings
import random

class BaseWorkerApp(object):
    def __init__(self, *args):
        self.registered_tasks=[]

    def init_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.download_root_path = path

    def init_logging(self):
        logging.config.dictConfig(settings.LOGGING)

    def init_app(self, path):
        self.init_logging()
        #self.init_path(path)

    def gather_tasks(self):
        return self.registered_tasks

    def register_task(self, func_task):
        self.registered_tasks.append(func_task)

    async def produce(self, queue, n=10):
        for x in range(n):
            # produce an item
            print('producing {}/{}'.format(x, n))
            # simulate i/o operation using sleep
            await asyncio.sleep(random.random())
            item = str(x)
            # put the item in the queue
            await queue.put(item)

    async def consume(self, queue):
        while True:
            # wait for an item from the producer
            item = await queue.get()

            # process the item
            print('consuming {}...'.format(item))
            # simulate i/o operation using sleep
            await asyncio.sleep(random.random())

            # Notify the queue that the item has been processed
            queue.task_done()

    async def run(self):
        queue = asyncio.Queue()

        # schedule the consumer
        consumer = asyncio.ensure_future(self.consume(queue))

        # run the producer and wait for completion
        await self.produce(queue)
        # wait until the consumer has processed all items
        await queue.join()
        # the consumer is still awaiting for an item, cancel it
        consumer.cancel()


def main(argv):
    try:
        parser = argparse.ArgumentParser(description="app server")
        parser.add_argument('--host')
        parser.add_argument('--path')
        parser.add_argument('--port')
        parser.add_argument('--media')

        # middle wares =[error_middleware]
        app = BaseWorkerApp()

        args = parser.parse_args()

        app.init_app(args.media)

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*app.gather_tasks()))

        # future = asyncio.Future()
        # asyncio.ensure_future(slow_operation(future))
        # future.add_done_callback(got_result)
        # try:
        #     loop.run_forever()
        # finally:
        #     loop.close()

    except KeyboardInterrupt:
        print("\nInterrupted")

if __name__ == "__main__":
    main(sys.argv)