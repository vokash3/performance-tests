import time
from typing import TypedDict

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from helpers.users.FakeUser import FakeUserFactory


class CreateUserRequestDict(TypedDict):
    """
    Структура данных для создания нового пользователя.
    """
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


# Добавили описание структуры пользователя
class UserDict(TypedDict):
    """
    Описание структуры пользователя.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


# Добавили описание структуры ответа получения пользователя
class GetUserResponseDict(TypedDict):
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserDict


# Добавили описание структуры ответа создания пользователя
class CreateUserResponseDict(TypedDict):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserDict


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
        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Создание нового пользователя.

        :param request: Словарь с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/users", json=request)

    # def get_user(self, user_id: str):
    #     """
    #     Получить данные пользователя по его user_id.
    #     :param user_id: str (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
    #     :return: httpx.Response
    #     """
    #     return self.client.get(f"/api/v1/users/{user_id}")

    def update_user(self, user_id: str, data: dict) -> Response:
        """
        Обновить данные пользователя.
        :param user_id: str (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :param data:
        :return: httpx.Response
        """
        return self.client.patch(f"/api/v1/users/{user_id}", json=data)

    def delete_user(self, user_id: str) -> Response:
        """
        Удалить пользователя.
        :param user_id: str (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: httpx.Response
        """
        return self.client.delete(f"/api/v1/users/{user_id}")

    # Добавили новый метод
    def get_user(self, user_id: str) -> GetUserResponseDict:
        """
        Обёртка для получения данных пользователя.
        :param user_id: Идентификатор пользователя. (ex: "06808055-dbf0-49d7-bab3-014aa01f8a73")
        :return: Ответ от сервера JSON с данными пользователя.
        """
        response = self.get_user_api(user_id)
        return response.json()

    # Добавили новый метод
    def create_user(self) -> CreateUserResponseDict:
        """
        Обёртка для создания нового пользователя.
        :return: Ответ от сервера JSON с данными нового пользователя.
        """
        fake_user = FakeUserFactory().create().to_payload()
        request = CreateUserRequestDict(**fake_user)
        response = self.create_user_api(request)
        return response.json()


# Добавляем builder для UsersGatewayHTTPClient
def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())
