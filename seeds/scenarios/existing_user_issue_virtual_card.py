from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedCardsPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга, который будет создавать 300 пользователей
    и открывать для каждого из них один дебетовый счёт с виртуальной картой.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        Возвращает план сидинга для создания пользователей и их дебетовых счетов (с вирт.картами).
        Мы создаём 300 пользователей, каждый откроет дебетовый счёт (с картой).
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Создаём 300 пользователей
                debit_card_accounts=SeedAccountsPlan(  # Дебетовый счёт на пользователя
                    count=1,
                    virtual_cards=SeedCardsPlan(count=1)  # С виртуальной картой
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Возвращает название сценария сидинга.
        Это имя будет использоваться для сохранения данных сидинга.
        """
        return "existing_user_issue_virtual_card"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.
    """
    import time

    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    print(f"Запуск сидинга {seeds_scenario.scenario}")
    start_time = time.time()
    seeds_scenario.build()  # Запуск сидинга
    end_time = time.time()
    print(f"Время выполнения сидинга: {end_time - start_time:.2f} секунд")
