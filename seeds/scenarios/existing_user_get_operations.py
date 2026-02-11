from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Cидинг для сценария получения информации об операциях
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        Возвращает план сидинга, который будет создавать 300 пользователей,
        открывать для каждого пользователя кредитный счёт,
        а затем выполнять для каждого пользователя следующее:

        - 5 операций покупки.
        - 1 операция пополнения счёта.
        - 1 операция снятия наличных.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Создаём 300 пользователей
                credit_card_accounts=SeedAccountsPlan(  # Кредитный счёт на пользователя
                    count=1,  # 1 счёт, на котором
                    purchase_operations=SeedOperationsPlan(count=5),  # 5 операций покупки,
                    top_up_operations=SeedOperationsPlan(count=1),  # 1 операция пополнения счёта,
                    cash_withdrawal_operations=SeedOperationsPlan(count=1),  # 1 операция снятия наличных.
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Возвращает название сценария сидинга.
        Это имя будет использоваться для сохранения данных сидинга.
        """
        return "existing_user_get_operations"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.
    """
    import time

    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    print(f"Запуск сидинга {seeds_scenario.scenario}")
    start_time = time.time()
    seeds_scenario.build()  # Запуск сидинга
    end_time = time.time()
    print(f"Время выполнения сидинга: {end_time - start_time:.2f} секунд")
