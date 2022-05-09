from locust import HttpUser, task, between, tag


class MyUser(HttpUser):
    host = "http://127.0.0.1:8081"
    wait_time = between(0.1, 0.5)

    @tag("nlu")
    @task(1)
    def nlu_request(self):
        post_data = {
            "question": "你好"
        }
        with self.client.post('/nlu', json=post_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Got wrong response")

    @tag("questions")
    @task(1)
    def questions_request(self):
        with self.client.get('/questions', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Got wrong response")
