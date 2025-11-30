from locust import HttpUser, task, between
import random

TOTAL_USERS = 1000

class TimelineUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        # Chaque utilisateur Locust aura un user différent
        self.user_id = random.randint(1, TOTAL_USERS)

    @task
    def get_timeline(self):
        self.client.get(f"/api/timeline?user=user{self.user_id}")
