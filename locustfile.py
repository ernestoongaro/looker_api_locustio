import yaml
from locust import HttpLocust, TaskSet, task
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ApiBehavior(TaskSet):

    def on_start(self):
        global options
        f = open('config.yml')
        params = yaml.load(f)
        f.close()
        host_yaml_node = self.locust.host
        self.hostname = params['hosts'][host_yaml_node]['host']
        self.token = params['hosts'][host_yaml_node]['token']
        self.secret = params['hosts'][host_yaml_node]['secret']
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        url = '{}{}'.format(self.hostname, 'login')
        params = {'client_id': self.token,
                  'client_secret': self.secret}
        with self.client.post(url, params=params, catch_response=True, verify=False) as r:
            access_token = r.json().get('access_token')
            # print('Access token: ' + access_token)

        self.client.headers.update({'Authorization': 'token {}'.format(access_token)})

    def logout(self):
        return

    @task(1)
    def get_look(self):
        # Choose a random look to retrieve results for:
        max_look_id = 10  # This is the maximum look ID on my instance - update it as appropriate
        look_to_get = random.randint(1, max_look_id)
        url = '{}{}/{}/run/{}'.format(self.hostname, 'looks', look_to_get, 'json')

        params = {'limit': 100000}
        with self.client.get(url, params=params, stream=True) as r:
            if r.status_code == requests.codes.ok:
                print(url + ': success (200)')
            else:
                print(url + ': failure (' + str(r.status_code) + ')')

class ApiUser(HttpLocust):
    task_set = ApiBehavior
    min_wait = 5000
    max_wait = 9000
