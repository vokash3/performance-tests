import random

from locust import events, task
from locust.env import Environment
from locust.runners import MasterRunner, LocalRunner

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


# Хук инициализации — вызывается перед началом запуска нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    if isinstance(environment.runner, MasterRunner) or isinstance(environment.runner, LocalRunner):
        # Выполняем сидинг
        seeds_scenario.build()  # создаём пользователей, счета, карты и операции

    # Загружаем результат сидинга (из файла JSON)
    environment.seeds = seeds_scenario.load()


class GetOperationsTaskSet(GatewayHTTPTaskSet):
    seed_user: SeedUserResult  # Типизированная ссылка на данные из сидинга

    def on_start(self) -> None:
        super().on_start()
        # Получаем случайного пользователя из подготовленного списка
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(1)
    def get_accounts(self):
        # Получаем список счетов пользователя
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(6)
    def get_operations(self):
        # Получаем список операций по счётам
        self.operations_gateway_client.get_operations(
            account_id=random.choice(self.seed_user.credit_card_accounts).account_id
        )

    @task(3)
    def get_operations_summary(self):
        # Получение статистики по операциям
        self.operations_gateway_client.get_operations_summary(
            random.choice(self.seed_user.credit_card_accounts).account_id)


class GetOperationsScenarioUser(LocustBaseUser):
    host = "http://gs-performance.ru:8003"
    tasks = [GetOperationsTaskSet]
