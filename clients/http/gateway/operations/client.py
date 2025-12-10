# 7.4 Реализация HTTP API клиентов
import datetime
import random
from typing import TypedDict

import httpx
from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.schema import CreateUserRequestSchema
from helpers.json_output import JSONOutput
from helpers.users.FakeUser import FakeUserFactory


# ====== TypedDict-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ ======

class OperationDict(TypedDict):
    id: str
    type: str
    status: str
    amount: float
    card_id: str
    category: str
    created_at: str
    account_id: str


class OperationReceiptDict(TypedDict):
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationsSummaryResponseDict(TypedDict):
    summary: OperationsSummaryDict


class GetOperationsResponseDict(TypedDict):
    operations: list[OperationDict]


class GetOperationResponseDict(TypedDict):
    operation: OperationDict


class GetOperationReceiptResponseDict(TypedDict):
    operation: OperationReceiptDict


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


class MakeFeeOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции комиссии.
    """
    operation: OperationDict


class MakeTopUpOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции пополнения.
    """


class MakeTopUpOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции пополнения.
    """
    operation: OperationDict


class MakeCashbackOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции кэшбэка.
    """


class MakeCashbackOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции кэшбэка.
    """
    operation: OperationDict


class MakeTransferOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции перевода.
    """


class MakeTransferOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции перевода.
    """
    operation: OperationDict


class MakePurchaseOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции покупки.
    """
    category: str


class MakePurchaseOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции покупки.
    """
    operation: OperationDict


class MakeBillPaymentOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции оплаты по счёту.
    """


class MakeBillPaymentOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции оплаты по счёту.
    """
    operation: OperationDict


class MakeCashWithdrawalOperationRequestDict(BaseOperationRequestDict):
    """
    Структура тела запроса для создания операции снятия наличных.
    """


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """
    Структура ответа на создание операции снятия наличных.
    """
    operation: OperationDict


# ====== (END) TypedDict-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ (END) ======


# ====== КЛИЕНТ (ОСНОВНОЙ КЛАСС) == ДЛЯ ВЗАИМОДЕЙСТВИЯ С /api/v1/operations ====
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

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """
        WRAPPER: Выполняет GET-запрос для получения информации об операции по её идентификатору.

        :param operation_id:str – Идентификатор операции. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationResponseDict
        """
        request = GetOperationPathParamsDict(operation_id=operation_id)
        response = self.get_operation_api(request)
        return response.json()

    def get_operation_receipt_api(self, path: GetOperationReceiptPathParamsDict) -> Response:
        """
        Выполняет GET-запрос для получения чека по операции.

        :param path: Словарь с параметрами пути, содержащий operation_id.
        :return: Объект httpx.Response с данными чека по операции.
        """
        operation_id = path["operation_id"]
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """
        WRAPPER: Выполняет GET-запрос для получения чека по операции.
        :param operation_id: str – Идентификатор операции. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationResponseDict
        """
        request = GetOperationReceiptPathParamsDict(operation_id=operation_id)
        response = self.get_operation_receipt_api(request)
        return response.json()

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения списка операций по указанному счёту.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Объект httpx.Response со списком операций.
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """
        WRAPPER: Выполняет GET-запрос для получения списка операций по указанному счёту.
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationsResponseDict
        """
        request = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(request)
        return response.json()

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения статистики по операциям по указанному счёту.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Объект httpx.Response с агрегированной статистикой по операциям.
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """
        WRAPPER: Выполняет GET-запрос для получения статистики по операциям по указанному счёту.
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationsSummaryResponseDict
        """
        request = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(request)
        return response.json()

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции комиссии.

        :param request: Словарь, основанный на BaseOperationRequestDict,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции комиссии.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeFeeOperationResponseDict
        """
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.

        :param request: Словарь, основанный на BaseOperationRequestDict,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции пополнения.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeTopUpOperationResponseDict
        """
        request = MakeTopUpOperationRequestDict(cardId=card_id, accountId=account_id, amount=55.77, status="COMPLETED")
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции кэшбэка.

        :param request: Словарь, основанный на BaseOperationRequestDict,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_cashback_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                status: str = "COMPLETED") -> MakeCashbackOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции кэшбэка.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeCashbackOperationResponseDict
        """
        request = MakeCashbackOperationRequestDict(cardId=card_id, accountId=account_id, amount=amount,
                                                   status=status)
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции перевода.

        :param request: Словарь, основанный на BaseOperationRequestDict,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_transfer_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                status: str = "COMPLETED") -> MakeTransferOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции перевода.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeTransferOperationResponseDict
        """
        request = MakeTransferOperationRequestDict(cardId=card_id, accountId=account_id, amount=amount,
                                                   status=status)
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции покупки.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полями category.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_purchase_operation(self, card_id: str, account_id: str, amount: float = 55.77, status: str = "COMPLETED",
                                category: str = "Learning") -> MakePurchaseOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции покупки.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakePurchaseOperationResponseDict
        """
        request = MakePurchaseOperationRequestDict(cardId=card_id, accountId=account_id, amount=amount,
                                                   status=status, category=category)
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции оплаты по счёту.

        :param request: Словарь, основанный на BaseOperationRequestDict,
                        дополненный полями billId и provider.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_bill_payment_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                    status: str = "COMPLETED") -> MakeBillPaymentOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции оплаты по счёту.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :param amount: float – Сумма операции. (например, 55.77)
        :param status: str – Статус операции. (например, "COMPLETED")
        :return: JSON -> MakeBillPaymentOperationResponseDict
        """
        request = MakeBillPaymentOperationRequestDict(cardId=card_id, accountId=account_id, amount=amount,
                                                      status=status)
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции снятия наличных.

        :param request: Словарь, основанный на BaseOperationRequestDict,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                       status: str = "COMPLETED") -> MakeCashWithdrawalOperationResponseDict:
        """
        WRAPPER: Выполняет POST-запрос для создания операции снятия наличных.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :param amount: float – Сумма операции. (например, 55.77)
        :param status: str – Статус операции. (например, "COMPLETED")
        :return: JSON -> MakeCashWithdrawalOperationResponseDict
        """
        request = MakeCashWithdrawalOperationRequestDict(cardId=card_id, accountId=account_id, amount=amount,
                                                         status=status)
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()


# Добавляем builder для OperationsGatewayHTTPClient – 7.5
def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())


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
        create_user_request: CreateUserRequestSchema = CreateUserRequestSchema(**fake_user.to_payload())
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
        cards = debit_data.get("account", {}).get("cards") or []
        if not cards:
            raise RuntimeError("NO CARDS!")

        card = random.choice(cards)
        card_id = card["id"]
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
