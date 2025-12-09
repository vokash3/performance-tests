# 7.4 Реализация HTTP API клиентов
import random
from typing import TypedDict

import httpx
from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.users.client import CreateUserRequestDict
from helpers.json_output import JSONOutput
from helpers.users.FakeUser import FakeUserFactory


# ====== TypedDict-структуры запросов и параметров ======

class GetOperationPathParamsDict(TypedDict):
    """
    Структура параметров пути для получения информации об операции.
    """
    operation_id: str


class GetOperationReceiptPathParamsDict(TypedDict):
    """
    Структура параметров пути для получения чека по операции.
    """
    operation_id: str


class GetOperationsQueryDict(TypedDict):
    """
    Параметры запроса для получения списка операций по счёту.
    """
    accountId: str


class GetOperationsSummaryQueryDict(TypedDict):
    """
    Параметры запроса для получения статистики по операциям по счёту.
    """
    accountId: str


class BaseOperationRequestDict(TypedDict):
    """
    Базовая структура тела запроса для создания операции.
    """
    status: str
    amount: float
    accountId: str
    cardId: str


class MakeFeeOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции комиссии.
    """


class MakeTopUpOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции пополнения.
    """


class MakeCashbackOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции кэшбэка.
    """


class MakeTransferOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции перевода.
    """


class MakePurchaseOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции покупки.
    """
    category: str


class MakeBillPaymentOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции оплаты по счёту.
    """


class MakeCashWithdrawalOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции снятия наличных.
    """


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, path: GetOperationPathParamsDict) -> Response:
        """
        Выполняет GET-запрос для получения информации об операции по её идентификатору.

        :param path: Словарь с параметрами пути, содержащий operation_id.
        :return: Объект httpx.Response с данными об операции.
        """
        operation_id = path["operation_id"]
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, path: GetOperationReceiptPathParamsDict) -> Response:
        """
        Выполняет GET-запрос для получения чека по операции.

        :param path: Словарь с параметрами пути, содержащий operation_id.
        :return: Объект httpx.Response с данными чека по операции.
        """
        operation_id = path["operation_id"]
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения списка операций по указанному счёту.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Объект httpx.Response со списком операций.
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения статистики по операциям по указанному счёту.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Объект httpx.Response с агрегированной статистикой по операциям.
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции комиссии.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полем feeType.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полем sourceType.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции кэшбэка.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полем cashbackRate.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции перевода.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полем destinationAccountId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции покупки.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полями category и merchant.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции оплаты по счёту.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полями billId и provider.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции снятия наличных.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полем atmId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)


if __name__ == "__main__":
    """
        Для теста:
        1. Создаёт пользователя.
        2. Открывает дебетовый счёт/карту.
        3. Делает операцию пополнения.
        4. Получает чек по операции.
        """


    def create_http_client():
        return httpx.Client(base_url="http://155.212.171.137:8003", timeout=100)


    with create_http_client() as raw_client:
        from clients.http.gateway.users.client import UsersGatewayHTTPClient
        from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient

        users_client = UsersGatewayHTTPClient(raw_client)
        accounts_client = AccountsGatewayHTTPClient(raw_client)
        operations_client = OperationsGatewayHTTPClient(raw_client)

        # 1. Создание пользователя
        fake_user = FakeUserFactory().create()
        create_user_request: CreateUserRequestDict = CreateUserRequestDict(**fake_user.to_payload())
        create_user_resp = users_client.create_user_api(create_user_request)
        create_user_resp.raise_for_status()
        user_data = create_user_resp.json()
        user_id = user_data.get("id") or user_data.get("user", {}).get("id")
        print("*** Создан пользователь с ID:", user_id, "*** \n")
        print(JSONOutput.get_json(user_data))

        # 2. Открытие дебетового счёта/карты
        from clients.http.gateway.accounts.client import OpenDebitCardAccountRequestDict

        open_debit_request: OpenDebitCardAccountRequestDict = {
            "userId": user_id,
        }
        open_debit_resp = accounts_client.open_debit_card_account_api(open_debit_request)
        open_debit_resp.raise_for_status()
        debit_data = open_debit_resp.json()
        account_id = debit_data.get("account", {}).get("id")
        card_id = random.choice(debit_data.get("account", {}).get("cards", {})).get("id")
        print("*** Открыт дебетовый счёт с ID:", account_id, "и карта с ID:", card_id, "*** \n")
        print(JSONOutput.get_json(debit_data))

        # 3. Операция пополнения
        top_up_request: MakeTopUpOperationRequestDict = {
            "status": "IN_PROGRESS",
            "amount": 1000.0,
            "accountId": account_id,
            "cardId": card_id,
        }
        make_top_up_resp = operations_client.make_top_up_operation_api(top_up_request)
        make_top_up_resp.raise_for_status()
        top_up_data = make_top_up_resp.json()
        operation_id = top_up_data.get("operation", {}).get("id")
        print("*** Создана операция пополнения с ID:", operation_id, " *** \n")

        # 4. Чек по операции
        receipt_resp = operations_client.get_operation_receipt_api(
            {"operation_id": operation_id}
        )
        receipt_resp.raise_for_status()
        print("*** Чек по операции с ID:", operation_id, ": *** \n")
        print(receipt_resp.json())
