import json

import httpx
from locust.env import Environment

from clients.http.client import HTTPClient
from clients.http.gateway.cards.schema import IssuePhysicalCardResponseSchema, IssueVirtualCardRequestSchema, \
    IssueVirtualCardResponseSchema, IssuePhysicalCardRequestSchema, CardsPayloadSchema
from clients.http.gateway.client import build_gateway_http_client, build_gateway_locust_http_client


class CardsGatewayHTTPClient(HTTPClient):
    """
    API клиент для работы с эндпоинтами /api/v1/cards сервиса http-gateway
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> httpx.Response:
        """
        Метод для создания виртуальной карты пользователя.
        :param request: IssueVirtualCardRequestSchema – Pydantic model
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-virtual-card", json=request.model_dump(by_alias=True))

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> httpx.Response:
        """
        Метод для создания физической карты пользователя.
        :param request: IssuePhysicalCardResponseSchema – Pydantic model
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-physical-card", json=request.model_dump(by_alias=True))

    # Добавили новый метод
    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseSchema:
        """
        Обёртка для создания виртуальной карты пользователя.
        :param user_id: Идентификатор пользователя. (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :param account_id: Идентификатор аккаунта. (ex: "c4d14cc2-6764-4305-b7f1-1f643072e4d4")
        :return: JSON -> Pydantic model – IssueVirtualCardResponseSchema)
        """
        request = IssueVirtualCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    # Добавили новый метод
    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseSchema:
        """
        Обёртка для создания физической карты пользователя.
        :param user_id: Идентификатор пользователя. (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :param account_id: Идентификатор аккаунта. (ex: "c4d14cc2-6764-4305-b7f1-1f643072e4d4")
        :return: JSON -> Pydantic model – IssuePhysicalCardResponseSchema
        """
        request = IssuePhysicalCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)


# Добавляем builder для CardsGatewayHTTPClient
def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_cards_gateway_locust_http_client(environment: Environment) -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр CardsGatewayHTTPClient с хуками сбора метрик.
    """
    return CardsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))


if __name__ == "__main__":
    """Тестирование API клиента"""
    user_dict = {
        "user_id": "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60",
        "account_id": "c4d14cc2-6764-4305-b7f1-1f643072e4d4"
    }
    payload = IssueVirtualCardRequestSchema(**user_dict)
    test_card = build_cards_gateway_http_client()
    print(
        f"VIRTUAL CARD: {json.dumps(test_card.issue_virtual_card_api(payload).json(), sort_keys=True, indent=4, ensure_ascii=False)}")
    payload = IssuePhysicalCardRequestSchema(**user_dict)
    print(
        f"\nPHYSICAL_CARD: {json.dumps(test_card.issue_physical_card_api(payload).json(), sort_keys=True, indent=4, ensure_ascii=False)}")
