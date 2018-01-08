# coding=utf-8
import ujson
from aiohttp import web
from aiohttp import log as aiolog


def json_error(message):
    return web.Response(body=ujson.dumps({
        'status': False,
        'error': 0,
        'msg': message}).encode('utf-8'), content_type='application/json')

async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 404:
                return json_error(response.message)

            if response.status == 304 or (response.status < 300 ):
                # static-file success and 304 Found are debug-level
                log_method = aiolog.access_logger.debug
            elif response.status < 400:
                log_method = aiolog.access_logger.info
            elif response.status < 500:
                log_method = aiolog.access_logger.warning
            else:
                log_method = aiolog.access_logger.error

            if response.status >= 500 and response.status != 502:
                log_method(ujson.dumps(request.headers, indent=2))

            return response

        except web.HTTPException as ex:
            if ex.status == 404:
                return json_error(ex.reason)
            raise
    return middleware_handler


