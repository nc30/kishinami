#!/usr/bin/env python3

from logging import getLogger
import logging.config
import sys
import os

LOGLEVEL = 'DEBUG' if os.environ.get('DEBUG', False) else 'INFO'

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(filename)s:%(lineno)d %(name)s [%(levelname)s] %(message)s'
        },
        'file': {
            'format': '[%(asctime)s] %(name)s [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/kishinami/kishinami.log',
            'when': 'd',
            'encoding': 'utf-8',
            'backupCount': 3,
            'formatter': 'file'
        }
    },
    'loggers': {
        'kishinami': {
            'handlers': ['console', 'file'],
            'level': LOGLEVEL,
        },
        'naganami_mqtt': {
            'handlers': ['console', 'file'],
            'level': LOGLEVEL,
        }
    },
}
logging.config.dictConfig(DEFAULT_LOGGING)


logger = getLogger('kishinami')

from naganami_mqtt.awsiot import getAwsCredentialFromJson
from kishinami.base import Base
from kishinami.aws import Kishinami
credential = getAwsCredentialFromJson('/aws/iot.json')

logger.info('- Kishinami Start.')

blinks = Base()
blinks.start()

c = Kishinami(credential)
c.setBlinks(blinks)

if __name__ == '__main__':
    import signal
    def handler(signum, frame):
        logger.info('get TERM signal.')
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, handler)

    try:
        c.loop(block=True)

    except KeyboardInterrupt:
        sys.exit(0)

    finally:
        blinks.destroy()
        c.disconnect()
        logger.info('bye.')

sys.exit(1)
