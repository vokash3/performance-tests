# python -m locust -f locust_get_user_scenario.py --class-picker --processes 2 --csv reports/locust_get_user_scenario.csv --csv-full-history --json --json-file reports/locust_get_user_scenario --html reports/locust_get_user_scenario.html -u 300 -r 30 -t 1m

from locust import HttpUser, between, task, constant_pacing, User

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.fakers import fake  # генератор случайных данных


class GetUserScenarioUser(User):
    """
    Наследуемся от User вместо HttpUser/FastHttpUser,
    чтобы не создавать экземпляр встроенного HTTP клиента (Requests/geventhttpclient)
    и пользоваться только возможностями гринлетов Locust.
    """
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    # wait_time = between(1, 3)
    wait_time = constant_pacing(1)
    # Будет проигнорировано под капотом, так как уже зафиксировано в кастомном клиенте,
    # но оставляем, чтобы в UI не смущал указанный целевой хост
    host = "http://155.212.171.137:8003"

    # Поле, в котором будет храниться экземпляр нашего API клиента
    users_gateway_client: UsersGatewayHTTPClient
    # Поле, куда мы сохраним ответ после создания пользователя
    create_user_response: CreateUserResponseSchema

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        # Шаг 1: создаем API клиент, встроенный в экосистему Locust (с хуками и поддержкой сбора метрик)
        # Передаём self.environment – объект окружения Locust с данными о запросах,
        # которые используются в статистике генератора
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)

        # Шаг 2: создаем пользователя через API
        # Помним, что пайдентик сам создаст нужную модель с помощью default_factory
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        """
        Основная нагрузочная задача: получение информации о пользователе.
        Здесь мы выполняем GET-запрос к /api/v1/users/{user_id},
        используя кастомный API клиент на базе httpx.
        """
        self.users_gateway_client.get_user(self.create_user_response.user.id)
