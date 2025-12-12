from locust import HttpUser, between, task, constant_pacing


# !/bin/bash  python -m locust -f locust_basic_scenario.py --class-picker --processes 2 --csv report.csv --csv-full-history --json --json-file report --html report.html -u 10 -r 1 -t 1m

# Класс виртуального пользователя, который будет выполнять наши задачи
class BasicScenarioUser(HttpUser):
    # Устанавливаем время ожидания между задачами: случайное значение от 5 до 15 секунд
    # wait_time = between(5, 15)
    # Устанавливаем пэйсинг = 1 сек на задачу
    wait_time = constant_pacing(1)
    host = "https://postman-echo.com"

    # Задача с весом 2: GET-запрос на /get будет вызываться в два раза чаще, чем остальные
    @task(2)
    def get_data(self):
        self.client.get("/get")

    # Задача с весом 1: POST-запрос на /post
    @task(1)
    def post_data(self):
        self.client.post("/post")

    # Задача с весом 1: DELETE-запрос на /delete
    @task(1)
    def delete_data(self):
        self.client.delete("/delete")
