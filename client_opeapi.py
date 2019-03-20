import requests
import hmac
from hashlib import sha1
import xml.etree.ElementTree as ET
from time import sleep
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s')

class ClientOpeapi(object):
    api_endpoint = 'http://opeapi.ws.pho.to'
    def __init__(self, app_id, secret):
        self.app_id = app_id
        self.secret = str(secret).encode("utf-8")

    def template_process(self, image_url, template_name):
        data = '''
        <image_process_call>
            <owner>py-client-opeapi</owner>
            <image_url order="1">{}</image_url>
            <methods_list>
                <method order="1">
                <name>collage</name><params>template_name={}</params></method>
            </methods_list>
        </image_process_call>
        '''.format(image_url, template_name)
        request_id = self.add_task(data)
        return self.wait_result(request_id)

    def add_task(self, data):
        form = {
            'app_id': self.app_id,
            'data': data,
            'sign_data': hmac.new(self.secret,  str(data).encode("utf-8"), sha1).hexdigest()
        }
        endpoint = '{}/addtask'.format(self.api_endpoint)
        response = requests.post(endpoint, data=form)
        resp_body = response.text
        logging.info('resp: {}'.format(resp_body))
        self._check_error(resp_body)
        tree = ET.fromstring(resp_body)
        request_id = tree.findall('request_id')[0].text
        return request_id

    def wait_result(self, request_id):
        max_try = 240
        for i in range(0, max_try):
            endpoint = '{}/getresult?request_id={}'.format(self.api_endpoint, request_id)
            response = requests.get(endpoint)
            resp_body = response.text
            logging.info('resp: {}'.format(resp_body))

            self._check_error(resp_body)
            if self._check_in_progress(resp_body):
                sleep(0.5)
                continue

            tree = ET.fromstring(resp_body)
            result_url = tree.findall('result_url')[0].text
            return result_url
        raise Exception('Error Processing Request')


    def _check_error(self, resp_body):
        tree = ET.fromstring(resp_body)
        status = tree.findall('status')[0].text.upper()
        if status != 'OK' and self._check_in_progress(resp_body) == False:
            description = tree.findall('description')[0].text
            raise Exception(description)

    def _check_in_progress(self, resp_body):
        tree = ET.fromstring(resp_body)
        status = tree.findall('status')[0].text.upper()
        return status == 'INPROGRESS'
