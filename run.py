import logging
from logging.handlers import TimedRotatingFileHandler
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('/var/log/kishinami/kishinami.log', when='d', encoding='utf-8', backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

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
        c.disconnect()
        blinks.destroy()
        logger.info('bye.')

    finally:
        blinks.destroy()
        c.disconnect()
        logger.info('bye.')
