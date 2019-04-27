from logging import getLogger
logger = getLogger(__name__)

from naganami_mqtt.awsiot import AwsIotContoller, getAwsCredentialFromJson
from color import Color
import json

class Kishinami(AwsIotContoller):
    status = {
        'color': Color([255, 40, 0]).list
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
            self._shadow_update(reported=self.status, desired={'color': color})

        except (KeyError, TypeError, json.decoder.JSONDecodeError):
            return '{"error": true, "reason": "TypeError"}'

        except Exception as e:
            logger.exception(e)

    def delta_function(self, payload):
        r = {}
        for k, v in payload['state'].items():
            if k == 'color':
                try:
                    self.status[k] = Color(v).list
                except TypeError:
                    pass
            elif k in self.status.keys():
                self.status[k] = v
                continue
            r[k] = None

        self.blinks.setColor(self.status['color'])
        self._shadow_update(reported=self.status, desired=r)
