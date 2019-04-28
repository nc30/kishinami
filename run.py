import logging
logger = logging.getLogger('kishinami')
logger = logging.getLogger('kishinami')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from naganami_mqtt.awsiot import getAwsCredentialFromJson
from kishinami.base import Base
from kishinami.aws import Kishinami
credential = getAwsCredentialFromJson('/aws/iot.json')

c = Kishinami(credential, logger=logger)
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

