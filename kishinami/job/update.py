from logging import getLogger
logger = getLogger(__name__)

from naganami_mqtt.job import JobScenario

import subprocess
import json

class UpdateError(Exception):
    pass

class UpdateJob(JobScenario):

    def sequence1_update_dist(self, jobDocument, statusDetail):
        logger.info('execute update secuence')

        try:
            command = 'sudo /opt/kishinami/python/bin/pip3 install --upgrade --force "' + jobDocument['distFileUrl'] + '"'
            proc = subprocess.Popen(
                command,
                shell  = True,
                stdin  = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            r = proc.communicate()
            proc.wait()

            logger.debug(r)

            logger.info('update return code is %s', proc.returncode)
            if proc.returncode != 0:
                raise UpdateError()

            logger.info('success.')
        except UpdateError as e:
            logger.exception(e)
            self.changeStatus('FAILED')

        return True

    def sequence2_restart(self, jobDocument, statusDetails):
        logger.info('do it restart job')

        if statusDetails.get('is_restarted', False):
            logger.info('restarted success')
            return True

        self.statusDetails['is_restarted'] = True
        self.changeStatus('IN_PROGRESS')

        command = 'sleep 1; sudo systemctl restart kishinami'
        proc = subprocess.Popen(
            command,
            shell  = True,
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        proc.communicate()

        self.kill_my_self()


    @staticmethod
    def valid(document):
        logger.debug("valid secuence %s", document)
        return document.get('type', '') == 'update' and document.get('distFileUrl', None)
