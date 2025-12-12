# python -m locust -f locust_get_user_scenario.py --class-picker --processes 2 --csv report.csv --csv-full-history --json --json-file report --html report.html -u 300 -r 10 -t 1m

from locust import HttpUser, between, task, constant_pacing

from tools.fakers import fake  # генератор случайных данных


class GetUserScenarioUser(HttpUser):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    # wait_time = between(1, 3)
    wait_time = constant_pacing(1)
    host = "http://155.212.171.137:8003"

    # В этой переменной будем хранить данные созданного пользователя
    user_data: dict

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        request = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }
        response = self.client.post("/api/v1/users", json=request)

        # Сохраняем полученные данные, включая ID пользователя
        self.user_data = response.json()

    @task
    def get_user(self):
        """
        Основная нагрузочная задача: получение информации о пользователе.
        Здесь мы выполняем GET-запрос к /api/v1/users/{user_id}.
        """
        self.client.get(
            f"/api/v1/users/{self.user_data['user']['id']}",
            name="/api/v1/users/{user_id}"  # Явное указание имени группы запросов
        )
