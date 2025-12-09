from typing import TypedDict

from httpx import Response

from clients.http.client import HTTPClient


class CreateUserRequestDict(TypedDict):
    """
    Структура данных для создания нового пользователя.
    """
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


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

    def get_user(self, user_id: str):
        """
        Получить данные пользователя по его user_id.
        :param user_id: str (ex: a5e019b7-5e6e-4fc7-ab80-a22d05b68c60)
        :return: httpx.Response
        """
        return self.client.get(f"/api/v1/users/{user_id}")

    def update_user(self, user_id: str, data: dict) -> Response:
        """
        Обновить данные пользователя.
        :param user_id: str (ex: a5e019b7-5e6e-4fc7-ab80-a22d05b68c60)
        :param data:
        :return: httpx.Response
        """
        return self.client.patch(f"/api/v1/users/{user_id}", json=data)

    def delete_user(self, user_id: str) -> Response:
        """
        Удалить пользователя.
        :param user_id: str (ex: a5e019b7-5e6e-4fc7-ab80-a22d05b68c60)
        :return: httpx.Response
        """
        return self.client.delete(f"/api/v1/users/{user_id}")
