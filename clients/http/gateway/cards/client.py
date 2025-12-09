import json
from typing import TypedDict

import httpx

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class CardsPayloadDict(TypedDict):
    """
    Структура данных для создания новой кредитной карты пользователя.
    """
    userId: str
    accountId: str


class CardsGatewayHTTPClient(HTTPClient):
    """
    API клиент для работы с эндпоинтами /api/v1/cards сервиса http-gateway
    """

    def issue_virtual_card_api(self, request: CardsPayloadDict) -> httpx.Response:
        """
        Метод для создания виртуальной карты пользователя.
        :param request (CardsPayloadDict):
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: CardsPayloadDict) -> httpx.Response:
        """
        Метод для создания физической карты пользователя.
        :param request (CardsPayloadDict):
                        {
                          "userId": "string",
                          "accountId": "string"
                        }
        :return: httpx.Response from POST request
        """
        return self.post(url="/api/v1/cards/issue-physical-card", json=request)


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
