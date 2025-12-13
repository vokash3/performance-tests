# 7.4 Реализация HTTP API клиентов -> 7.5

from httpx import Response, QueryParams

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.accounts.schema import GetAccountsQuerySchema, OpenDepositAccountRequestSchema, \
    OpenSavingsAccountRequestSchema, OpenDebitCardAccountRequestSchema, OpenCreditCardAccountRequestSchema, \
    GetAccountsResponseSchema, OpenDepositAccountResponseSchema, OpenSavingsAccountResponseSchema, \
    OpenDebitCardAccountResponseSchema, OpenCreditCardAccountResponseSchema
from clients.http.gateway.client import build_gateway_http_client


class AccountsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """

    def get_accounts_api(self, query: GetAccountsQuerySchema):
        """
        Выполняет GET-запрос на получение списка счетов пользователя.

        :param query: Словарь с параметрами запроса, например: {'user_id': '123'}.
        :return: Объект httpx.Response с данными о счетах.
        """
        return self.get("/api/v1/accounts", params=QueryParams(query.model_dump()), extensions=HTTPClientExtensions(
            route="/api/v1/accounts"))  # Явно передаём логическое имя маршрута

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.

        :param request: Словарь с user_id.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post("/api/v1/accounts/open-deposit-account", json=request.model_dump(by_alias=True))

    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.

        :param request: Словарь с user_id.
        :return: Объект httpx.Response.
        """
        return self.post("/api/v1/accounts/open-savings-account", json=request.model_dump(by_alias=True))

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.

        :param request: Словарь с user_id.
        :return: Объект httpx.Response.
        """
        return self.post("/api/v1/accounts/open-debit-card-account", json=request.model_dump(by_alias=True))

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.

        :param request: Словарь с user_id.
        :return: Объект httpx.Response.
        """
        return self.post("/api/v1/accounts/open-credit-card-account", json=request.model_dump(by_alias=True))

    def get_accounts(self, user_id: str) -> GetAccountsResponseSchema:
        """
        Wrapper для get_accounts_api.
        :param user_id: str – идентификатор пользователя (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: JSON -> GetAccountsResponseSchema
        """
        query: GetAccountsQuerySchema = GetAccountsQuerySchema(user_id=user_id)
        response = self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseSchema:
        """
        Wrapper для open_deposit_account_api.
        :param user_id: str – идентификатор пользователя (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: JSON -> OpenDepositAccountResponseSchema
        """
        request = OpenDepositAccountRequestSchema(user_id=user_id)
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_savings_account(self, user_id: str) -> OpenSavingsAccountResponseSchema:
        """
        Wrapper для open_savings_account_api.
        :param user_id: str – идентификатор пользователя (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: JSON -> OpenSavingsAccountResponseSchema
        """
        request = OpenSavingsAccountRequestSchema(user_id=user_id)
        response = self.open_savings_account_api(request)
        return OpenSavingsAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseSchema:
        """
        Wrapper для open_debit_card_account_api.
        :param user_id: str – идентификатор пользователя (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: JSON -> OpenDebitCardAccountResponseSchema
        """
        request = OpenDebitCardAccountRequestSchema(user_id=user_id)
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseSchema:
        """
        Wrapper для open_credit_card_account_api.
        :param user_id: str – идентификатор пользователя (ex: "a5e019b7-5e6e-4fc7-ab80-a22d05b68c60")
        :return: JSON -> OpenCreditCardAccountResponseSchema
        """
        request = OpenCreditCardAccountRequestSchema(user_id=user_id)
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AccountsGatewayHTTPClient.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())
