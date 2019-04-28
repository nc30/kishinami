from logging import getLogger
logger = getLogger(__name__)

logger.debug('hello!')

from naganami_mqtt.awsiot import AwsIotContoller
from kishinami import NORMAL, WARNING, SILEN
from .color import Color
from threading import Thread
import json
import time

class Kishinami(AwsIotContoller):
    logger = logger
    status = {
        'color': Color([255, 40, 0]).list,
        'state': NORMAL,
        'check_span': 180,
        'noticeset': []
    }

    def setBlinks(self, blinks):
        self.blinks = blinks

    def on_connect(self, client, userdata, flags, respons_code):
        self._shadow_update(reported=self.status)
        self.client.on_disconnect = self.on_disconnect

    def on_disconnect(client, userdata, rc):
        logger.info('Connection lost.')

    def loop(self, block=True):
        self.logger.debug('loop start.')
        self.looping = True

        self.client.loop_start()
        i = 0
        while self.looping:
            i += 1
            if i > int(self.status['check_span']) * 10:
                self._shadow_update(self.status)
                i = 0
            time.sleep(0.1)

    def destroy(self):
        self.client.disconnect()
        self.looping = False

    def cmd_color(self, payload):
        try:
            payload = json.loads(payload)
            color = Color(payload['color']).list
            mask = payload.get('mask', 255)
            self._shadow_update(reported=self.status, desired={'color': color, 'mask': mask})

        except (KeyError, TypeError, json.decoder.JSONDecodeError):
            return '{"error": true, "reason": "TypeError"}'

        except Exception as e:
            logger.exception(e)

    def cmd_shock(self, payload):
        try:
            payload = json.loads(payload)
            color = Color(payload['color']).list
        except:
            color = [255, 40, 0]

        self.blinks.shock(color)

    def cmd_state(self, payload):
        if payload in [NORMAL, SILEN, WARNING]:
            self._shadow_update(desired={'state': payload})
            return {'success': True}
        return {'success': False}

    def delta_function(self, payload):
        r = {}
        for k, v in payload['state'].items():
            if k == 'color':
                try:
                    self.status[k] = Color(v).list
                    r[k] = self.status[k]
                except TypeError:
                    pass

            elif k == 'state':
                if v == NORMAL:
                    v = NORMAL
                elif v == SILEN:
                    v = SILEN
                else:
                    v = WARNING

                self.status[k] = v
                r[k] = v
                continue

            elif k in self.status.keys():
                self.status[k] = v
                continue
            r[k] = None


        self.blinks.setState(self.status['state'])
        if self.status['state'] == NORMAL:
            for i in range(0, 8):
                if i >= len(self.status['noticeset']):
                    break
                if type(self.status['noticeset'][i]) == list:
                    self.blinks.setColor(self.status['noticeset'][i], 1 << i)

        self._shadow_update(reported=self.status, desired=r)
