import time

from httpx import Response

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.schema import (  # Добавили импорт моделей
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)
from helpers.users.FakeUser import FakeUserFactory


# Старые модели с использованием TypedDict были удалены 10.12.2025

class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/users/{user_id}", extensions=HTTPClientExtensions(
            route="/api/v1/users/{user_id}"))  # Явно передаём логическое имя маршрута

    # Теперь используем pydantic-модель для аннотации
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.

        :param request: Pydantic-модель с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        # Сериализуем модель в словарь с использованием alias
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        # Инициализируем модель через валидацию JSON строки
        return GetUserResponseSchema.model_validate_json(response.text)

    # Теперь используем pydantic-модель для аннотации
    def create_user(self) -> CreateUserResponseSchema:
        # Генерация данных теперь происходит внутри схемы запроса
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        # Инициализируем модель через валидацию JSON строки
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())
