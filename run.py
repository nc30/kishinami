import logging
from logging.handlers import TimedRotatingFileHandler
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# handler = TimedRotatingFileHandler('log.log', when='d', encoding='utf-8', backupCount=3)
handler = logging.StreamHandler(stream=sys.stdout)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

from naganami_mqtt.awsiot import getAwsCredentialFromJson
from kishinami.base import Base
from kishinami.aws import Kishinami
credential = getAwsCredentialFromJson('/aws/iot.json')

c = Kishinami(credential)
blinks = Base()
blinks.start()

c.setBlinks(blinks)

if __name__ == '__main__':
    import signal
    def handler(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, handler)

    try:
        c.loop(block=True)

    except KeyboardInterrupt:
        c.disconnect()
        blinks.destroy()
        print('bye')

    finally:
        print('bye')
        blinks.destroy()
        c.disconnect()

