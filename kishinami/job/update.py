from logging import getLogger
logger = getLogger(__name__)

from naganami_mqtt.job import JobScenario

import urllib.request
import urllib.error
import subprocess
import json

url = 'https://s3-ap-northeast-1.amazonaws.com/kishinami/latest'

class UpdateError(Exception):
    pass

class UpdateJob(JobScenario):
    def exec(self, jobDocument):
        logger.debug('execute secuence')
        try:
            req = urllib.request.Request(url)
            try:
                with urllib.request.urlopen(req) as res:
                    body = res.read()
                    status = res.status
            except urllib.error.HTTPError:
                raise UpdateError()

            if status != 200:
                raise UpdateError()

            logger.debug(body)

            try:
                body = json.loads(body.decode())
            except Exception:
                raise UpdateError

            command = 'sudo /opt/kishinami/python/bin/pip3 install '+body['latest']['url']
            proc = subprocess.Popen(
                command,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            proc.communicate()
            proc.wait()

            logger.debug(proc.returncode)
            if proc.returncode != 0:
                raise UpdateError()

            self.changeStatus('SUCCEEDED')

            command = 'sudo systemctl restart kishinami'
            proc = subprocess.Popen(
                command,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            proc.communicate()

        except UpdateError as e:
            logger.exception(e)
            self.changeStatus('FAILED')

    @staticmethod
    def valid(document):
        logger.debug("valid secuence")
        return document.get('type', '') == 'update' and document.get('expectedVersion', None) == 'latest'
