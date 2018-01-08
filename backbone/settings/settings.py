# coding=utf-8
import os

APP_PORT = 8889
APP_HOST = '127.0.0.1'
APP_URL = "http://cache.FNMD.tk"
RESOURCE_PATH=""
LOG_DIR = "/Users/joshuaz/cache70/logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/server.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/server-error.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/server-request.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'aiohttp.access':{
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'aiohttp.client': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'aiohttp.server': {
            'handlers': ['error', 'console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}