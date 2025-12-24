# python -m locust -f grpc_locust_get_user_scenario.py \
#   --class-picker \
#   --processes 2 \
#   --csv reports/grpc_locust_get_user_scenario.csv \
#   --csv-full-history --json-file reports/grpc_locust_get_user_scenario \
#   --html reports/grpc_locust_get_user_scenario.html \
#   -u 300 -r 30 -t 1m
from locust import User, task, constant_pacing

from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class GetUserScenarioUser(User):
    """
    Класс (Locust User), описывающий сценарий нагрузочного тестирования для сервиса UsersGatewayService (ручка GetUser)
    """

    # Атрибут host обязателен для Locust, даже если он не используется напрямую в gRPC.
    host = "http://155.212.171.137:9003"
    # Время ожидания между задачами от 1 до 3 секунд.
    wait_time = constant_pacing(1)

    # Аннотации для клиентов и ответов
    users_gateway_client: UsersGatewayGRPCClient
    create_user_response: CreateUserResponse

    def on_start(self) -> None:
        """
        Метод, вызываемый при старте каждого виртуального пользователя.
        Здесь происходит инициализация gRPC API клиента и создание пользователя.
        """
        # Инициализируем gRPC-клиент, пригодный для Locust, с интерцептором метрик.
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)

        # Создаём пользователя один раз в начале сессии.
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        """
        Основная задача виртуального пользователя — получение данных пользователя.
        Метод будет многократно вызываться Locust-агентами.
        """
        self.users_gateway_client.get_user(self.create_user_response.user.id)
