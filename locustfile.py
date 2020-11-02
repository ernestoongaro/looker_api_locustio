import time,random,requests
import looker_sdk
from looker_sdk import models, error
from locust import User, task, between, events

class lookerStress(User):
    wait_time = between(30, 60)

    def on_start(self):
        self.sdk = looker_sdk.init31("looker.ini")

    def on_stop(self):
        self.sdk.logout()

    @task(1)
    def get_look(self):
        api_call_name = 'run_look'
        # Choose a random look to retrieve results for:
        look_ids = [5,6,7,8,9]
        look_to_get = random.choice(look_ids)
        start_time = time.time()
        try:
            self.sdk.run_look(look_to_get,'txt')
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                    request_type="GET", name=api_call_name, response_time=total_time, response_length=0
                    )
        except error.SDKError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                    request_type="GET", name=api_call_name, response_time=total_time, response_length=0, exception=e
                )

