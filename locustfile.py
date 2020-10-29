import yaml
from locust import HttpUser, TaskSet, task, User
import random
import requests

class ApiBehavior(TaskSet):

    def on_start(self):
        self.hostname = 'https://YOURS.cloud.looker.com/api/3.1/'
        self.secret = 'YOURS'
        self.token = 'YOURS'
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        url = '{}{}'.format(self.hostname, 'login')
        params = {'client_id': self.token,
                  'client_secret': self.secret}
        with self.client.post(url,
                              params=params,
                              catch_response=True) as r: # add verify=False if using a self-signed cert
            access_token = r.json().get('access_token')
        self.client.headers.update({'Authorization': 'token {}'.format(access_token)})

    def logout(self):
        self.client.delete(self.hostname+'logout')
        return

    @task(1)
    def get_look(self):
        # Choose a random look to retrieve results for:
        look_ids = [5,6,7,8,9]  
        look_to_get = random.choice(look_ids)
        url = '{}{}/{}/run/{}'.format(self.hostname, 'looks', look_to_get, 'txt')

        params = {'cache': 'false'}
        #with self.client.get(url, params=params, stream=True) as r:
        with self.client.get(url, params=params,timeout=60) as r:
            if r.status_code == requests.codes.ok:
                print(url + ': success (200)')
            else:
                print(url + ': failure (' + str(r.status_code) + str(r.reason) + ')')

class ApiUser(HttpUser):
    tasks = [ApiBehavior]
    min_wait = 10000
    max_wait = 60000
