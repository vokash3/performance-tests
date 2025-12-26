# python -m locust -f locust_get_accounts.py --headless --processes 4 --html reports/locust_get_accounts.html -u 50 -r 1 -t 1m
from locust import task, User, between, run_single_user, constant_pacing

from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """
    Нагрузочный сценарий, который в соответствии с указанными весами
    1. Создаёт нового пользователя.
    2. Открывает депозитный счёт.
    3. Запрашивает список всех счетов для текущего пользователя.

    Использует базовый GatewayHTTPTaskSet и уже созданных в нём API клиентов.
    """
    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponseSchema | None = None

    @task(2)
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для других тасок.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """
        Выполняет запрос на открытие депозитного счёта.
        Должна выполняться только в том случае, если в shared state уже есть данные о пользователе (user.id).
        :return:
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать
        self.accounts_gateway_client.open_deposit_account(user_id=self.create_user_response.user.id)

    @task(6)
    def get_accounts(self):
        """
        Запрашивает список всех счетов для текущего пользователя.
        Также должна выполняться только при наличии данных о пользователе (user.id).
        :return:
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать

        self.accounts_gateway_client.get_accounts(user_id=self.create_user_response.user.id)


class GetAccountsScenarioUser(User):
    """
    Пользователь Locust, исполняющий задачи из GetAccountsTaskSet.
    """
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = constant_pacing(1)  # Шаг – вместо случайной задержки
