import time
from dataclasses import dataclass, asdict
from typing import List
from faker import Faker

fake = Faker("ru_RU")


@dataclass
class FakeUser:
    """Фейковый пользователь."""
    email: str
    firstName: str
    lastName: str
    middleName: str
    phoneNumber: str

    def to_payload(self) -> dict:
        """Готовый dict для запросов."""
        return asdict(self)


class FakeUserFactory:
    """Создание тестовых пользователей.
    Для генерации фейкового пользователя – create(),
    При отправке запроса в API – to_payload().
    Для создания пачки пользователей – create_batch() – List.
    """

    def __init__(self, faker: Faker | None = None) -> None:
        self.fake = faker or fake

    def create(self) -> FakeUser:
        """Генерирует фейкового пользователя."""
        now = time.time()
        return FakeUser(
            email=f"user_{now}@example.com",
            lastName=self.fake.last_name_male(),
            firstName=self.fake.first_name_male(),
            middleName=self.fake.middle_name_male(),
            phoneNumber=self.fake.phone_number(),
        )

    def create_batch(self, size: int) -> List[FakeUser]:
        """Генерирует пачку фейковых пользователей."""
        return [self.create() for _ in range(size)]
