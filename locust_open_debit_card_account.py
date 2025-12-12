# python -m locust -f locust_open_debit_card_account.py --class-picker --processes 2 --csv reports/report.csv --csv-full-history --json-file reports/report --html reports/report_$(date +"%d%m%Y_%H%M").html -u 300 -r 10 -t 1m

from locust import HttpUser, between, task, constant_pacing

from tools.fakers import fake  # генератор случайных данных


class OpenDebitCardAccountScenarioUser(HttpUser):
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
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: операция создания дебетового счёта.
        Здесь мы выполняем POST-запрос к /api/v1/accounts/open-debit-card-account с телом
        {
            "userId": str(uuid4)
        }
        """
        self.client.post(
            f"/api/v1/accounts/open-debit-card-account",
            name="/api/v1/accounts/open-debit-card-account",  # Явное указание имени группы запросов
            json={"userId": self.user_data['user']['id']},
        )
