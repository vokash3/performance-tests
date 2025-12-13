# 7.4 Реализация HTTP API клиентов

from httpx import Response

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.documents.schema import GetTariffDocumentResponseSchema


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифа по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}",
                        extensions=HTTPClientExtensions(route="/api/v1/documents/tariff-document/{account_id}"))

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контракта по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}",
                        extensions=HTTPClientExtensions(route="/api/v1/documents/contract-document/{account_id}"))

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Обёртка для get_tariff_document_api: Получить тариф по счету.
        :param account_id: str – Идентификатор счета (например, "c4d14cc2-6764-4305-b7f1-1f643072e4d4").
        :return: JSON -> GetTariffDocumentResponseSchema – PyDantic модель
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Обёртка для get_contract_document_api: Получить контракт по счету.
        :param account_id: str – Идентификатор счета (например, "c4d14cc2-6764-4305-b7f1-1f643072e4d4").
        :return: JSON -> GetContractDocumentResponseSchema – PyDantic модель
        """
        response = self.get_contract_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)


# Добавляем builder для DocumentsGatewayHTTPClient
def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
