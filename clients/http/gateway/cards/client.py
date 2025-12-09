import json
from typing import TypedDict

import httpx

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


# Добавили описание структуры карты
class CardDict(TypedDict):
    """
    Описание структуры карты.
    """
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    accountId: str
    cardNumber: str
    cardHolder: str
    expiryDate: str
    paymentSystem: str


class CardsPayloadDict(TypedDict):
    """
    FIXME: к удалению (дублирует IssueVirtualCardRequestDict) из пункта 7.5
    Структура данных для создания новой кредитной карты пользователя.
    """
    userId: str
    accountId: str


class IssueVirtualCardRequestDict(TypedDict):
    """
    Структура данных для выпуска виртуальной карты.
    """
    userId: str
    accountId: str


# Добавили описание структуры ответа выпуска виртуальной карты
class IssueVirtualCardResponseDict(TypedDict):
    """
    Описание структуры ответа выпуска виртуальной карты.
    """
    card: CardDict


class IssuePhysicalCardRequestDict(TypedDict):
    """
    Структура данных для выпуска физической карты.
    """
    userId: str
    accountId: str


# Добавили описание структуры ответа выпуска физической карты
class IssuePhysicalCardResponseDict(TypedDict):
    """
    Описание структуры ответа выпуска физической карты.
    """
    card: CardDict


class CardsGatewayHTTPClient(HTTPClient):
    """
    API клиент для работы с эндпоинтами /api/v1/cards сервиса http-gateway
    """

    def issue_virtual_card_api(self, request: CardsPayloadDict | IssueVirtualCardRequestDict) -> httpx.Response:
        """
        Метод для создания виртуальной карты пользователя.
        :param request (CardsPayloadDict|IssueVirtualCardRequestDict):
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: CardsPayloadDict | IssueVirtualCardRequestDict) -> httpx.Response:
        """
        Метод для создания физической карты пользователя.
        :param request (CardsPayloadDict | IssueVirtualCardRequestDict):
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-physical-card", json=request)

    # Добавили новый метод
    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:
        """
        Обёртка для создания виртуальной карты пользователя.
        :param user_id: Идентификатор пользователя. (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :param account_id: Идентификатор аккаунта. (ex: "c4d14cc2-6764-4305-b7f1-1f643072e4d4")
        :return: JSON -> dict(IssueVirtualCardResponseDict)
        """
        request = IssueVirtualCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_virtual_card_api(request)
        return response.json()

    # Добавили новый метод
    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:
        """
        Обёртка для создания физической карты пользователя.
        :param user_id: Идентификатор пользователя. (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :param account_id: Идентификатор аккаунта. (ex: "c4d14cc2-6764-4305-b7f1-1f643072e4d4")
        :return: JSON -> dict(IssuePhysicalCardResponseDict)
        """
        request = IssuePhysicalCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_physical_card_api(request)
        return response.json()


# Добавляем builder для CardsGatewayHTTPClient
def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())


if __name__ == "__main__":
    """Тестирование API клиента"""
    payload = CardsPayloadDict(userId="a5e019b7-5e6e-4fc7-ab80-a22d05b68c60",
                               accountId="c4d14cc2-6764-4305-b7f1-1f643072e4d4")
    test_card = build_cards_gateway_http_client()
    print(
        f"VIRTUAL CARD: {json.dumps(test_card.issue_virtual_card_api(payload).json(), sort_keys=True, indent=4, ensure_ascii=False)}")
    print(
        f"\nPHYSICAL_CARD: {json.dumps(test_card.issue_physical_card_api(payload).json(), sort_keys=True, indent=4, ensure_ascii=False)}")
