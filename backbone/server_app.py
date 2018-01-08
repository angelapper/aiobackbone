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


class BaseServerApp(web.Application):
    def init_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.download_root_path = path

    def init_logging(self):
        logging.config.dictConfig(settings.LOGGING)

    def init_app(self, path):
        self.init_logging()
        self.init_path(path)


def main(argv):
    async def start_background_tasks(app):
        pass

    async def cleanup_background_tasks(app):
        pass

    try:
        parser = argparse.ArgumentParser(description="app server")
        parser.add_argument('--host')
        parser.add_argument('--path')
        parser.add_argument('--port')
        parser.add_argument('--media')

        # middlewares =[error_middleware]
        app = BaseServerApp()
        app.on_startup.append(start_background_tasks)
        app.on_cleanup.append(cleanup_background_tasks)

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        args = parser.parse_args()
        if args.media is None:
            args.media = "images"

        app.init_app(args.media)

        if args.port is None:
            args.port = 8889

        if args.host is None:
            args.host = "127.0.0.1"

        if args.path:
            web.run_app(app, path=args.path)
        else:
            web.run_app(app, path=args.path, host=args.host, port=int(args.port))

    except KeyboardInterrupt:
        print("\nInterrupted")

if __name__ == "__main__":
    main(sys.argv)