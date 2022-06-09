from locust import HttpUser, TaskSet, task, between
from datetime import datetime

now = datetime.now()


class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def login(self):
        response = self.client.get("dancing")

    @task(2)
    def practice(self):
        response = self.client.get("practice")
