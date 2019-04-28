from logging import getLogger
logger = getLogger(__name__)

from naganami_mqtt.awsiot import AwsIotContoller
from kishinami import NORMAL, WARNING, SILEN
from .color import Color
import json

class Kishinami(AwsIotContoller):
    status = {
        'color': Color([255, 40, 0]).list,
        'mask': 255,
        'state': NORMAL
    }

    def setBlinks(self, blinks):
        self.blinks = blinks

    def on_connect(self, client, userdata, flags, respons_code):
        self._shadow_update(reported=self.status)
        self.client.on_disconnect = self.on_disconnect

    def on_disconnect(client, userdata, rc):
        pass

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
            color = [255, 0, 0]

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

            if k == 'state':
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

        self.blinks.setColor(self.status['color'], self.status['mask'])
        self.blinks.setState(self.status['state'])
        self._shadow_update(reported=self.status, desired=r)
