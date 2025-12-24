# python -m locust -f grpc_locust_open_debit_card_account.py --class-picker --processes 4 --html reports/grpc_locust_open_debit_card_account_report_$(date +"%d%m%Y_%H%M").html -u 100 -r 10 -t 3m

from locust import task, User, between

from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.users.schema import CreateUserResponseSchema


class OpenDebitCardAccountScenarioUser(User):
    """
    Класс, описывающий сценарий нагрузочного тестирования для gRPC-запроса OpenDebitCardAccount.
    """
    wait_time = between(1, 3)
    host = "http://155.212.171.137:9003"

    users_gateway_client: UsersGatewayGRPCClient
    create_user_response: CreateUserResponseSchema

    accounts_gateway_client: AccountsGatewayGRPCClient
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema

    def on_start(self) -> None:
        """
        Выполняется при старте виртуального пользователя.
        Создание нового пользователя в системе и сохранение полученных объектов в self.create_user_response
        через кастомный клиент UsersGatewayGRPCClient + инициализация AccountsGatewayGRPCClient.
        :return:
        """
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: операция создания дебетового счёта.
        Здесь мы выполняем gRPC-запрос на ручку OpenDebitCardAccount
        {
            "userId": str(uuid4)
        }
        через кастомный клиент AccountsGatewayGRPCClient.
        Инициализация AccountsGatewayGRPCClient в on_start(),
        чтобы избежать создания нового клиента (объекта для каждого запроса.
        """
        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            self.create_user_response.user.id)
