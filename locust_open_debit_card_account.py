# python -m locust -f locust_open_debit_card_account.py --class-picker --processes 2 --csv reports/report.csv --csv-full-history --json-file reports/report --html reports/report_$(date +"%d%m%Y_%H%M").html -u 300 -r 10 -t 1m

from locust import task, constant_pacing, User

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.users.client import build_users_gateway_locust_http_client, UsersGatewayHTTPClient
from clients.http.gateway.users.schema import CreateUserResponseSchema


class OpenDebitCardAccountScenarioUser(User):
    wait_time = constant_pacing(1)
    host = "http://155.212.171.137:8003"

    users_gateway_client: UsersGatewayHTTPClient
    create_user_response: CreateUserResponseSchema

    accounts_gateway_client: AccountsGatewayHTTPClient
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema

    def on_start(self) -> None:
        """
        Выполняется при старте виртуального пользователя.
        Создание нового пользователя в системе и сохранение полученных объектов в self.create_user_response
        через кастомный клиент UsersGatewayHTTPClient
        :return:
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: операция создания дебетового счёта.
        Здесь мы выполняем POST-запрос к /api/v1/accounts/open-debit-card-account с телом
        {
            "userId": str(uuid4)
        }
        через кастомный клиент AccountsGatewayHTTPClient
        """
        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            self.create_user_response.user.id)
