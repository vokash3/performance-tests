# 7.4 Реализация HTTP API клиентов
import random

import httpx
from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.operations.schema import *
from clients.http.gateway.users.schema import CreateUserRequestSchema
from helpers.json_output import JSONOutput


# ====== КЛИЕНТ (ОСНОВНОЙ КЛАСС) == ДЛЯ ВЗАИМОДЕЙСТВИЯ С /api/v1/operations ====
class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, path: GetOperationPathParamsSchema) -> Response:
        """
        Выполняет GET-запрос для получения информации об операции по её идентификатору.

        :param path: Словарь с параметрами пути, содержащий operation_id.
        :return: Объект httpx.Response с данными об операции.
        """
        operation_id = path.operation_id
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        """
        WRAPPER: Выполняет GET-запрос для получения информации об операции по её идентификатору.

        :param operation_id:str – Идентификатор операции. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationResponseSchema
        """
        request = GetOperationPathParamsSchema(operation_id=operation_id)
        response = self.get_operation_api(request)
        return GetOperationResponseSchema.model_validate_json(response.text)

    def get_operation_receipt_api(self, path: GetOperationReceiptPathParamsSchema) -> Response:
        """
        Выполняет GET-запрос для получения чека по операции.

        :param path: Словарь с параметрами пути, содержащий operation_id.
        :return: Объект httpx.Response с данными чека по операции.
        """
        operation_id = path.operation_id
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseSchema:
        """
        WRAPPER: Выполняет GET-запрос для получения чека по операции.
        :param operation_id: str – Идентификатор операции. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationResponseSchema
        """
        request = GetOperationReceiptPathParamsSchema(operation_id=operation_id)
        response = self.get_operation_receipt_api(request)
        return GetOperationReceiptResponseSchema.model_validate_json(response.text, by_alias=True)

    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        """
        Выполняет GET-запрос для получения списка операций по указанному счёту.

        :param query: PyDantic модель параметров запроса, например: {'account_id': '123'}.
        :return: Объект httpx.Response со списком операций.
        """
        return self.get("/api/v1/operations", params=QueryParams(
            GetOperationsQuerySchema.model_dump(query, by_alias=True)))

    def get_operations(self, account_id: str) -> GetOperationsResponseSchema:
        """
        WRAPPER: Выполняет GET-запрос для получения списка операций по указанному счёту.
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationsResponseSchema
        """
        request = GetOperationsQuerySchema(account_id=account_id)
        response = self.get_operations_api(request)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        """
        Выполняет GET-запрос для получения статистики по операциям по указанному счёту.

        :param query: PyDantic модель параметров запроса, например: {'account_id': '123'}.
        :return: Объект httpx.Response с агрегированной статистикой по операциям.
        """
        return self.get("/api/v1/operations/operations-summary",
                        params=QueryParams(GetOperationsSummaryQuerySchema.model_dump(query, by_alias=True)))

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseSchema:
        """
        WRAPPER: Выполняет GET-запрос для получения статистики по операциям по указанному счёту.
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> GetOperationsSummaryResponseSchema
        """
        request = GetOperationsSummaryQuerySchema(account_id=account_id)
        response = self.get_operations_summary_api(request)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)

    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции комиссии.

        :param request: PyDantic модель BaseOperationRequestSchema,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request.model_dump(by_alias=True))

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции комиссии.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeFeeOperationResponseSchema
        """
        request = MakeFeeOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_fee_operation_api(request)
        return MakeFeeOperationResponseSchema.model_validate_json(response.text)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.

        :param request: PyDantic модель BaseOperationRequestSchema,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request.model_dump(by_alias=True))

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции пополнения.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeTopUpOperationResponseSchema
        """
        request = MakeTopUpOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_top_up_operation_api(request)
        return MakeTopUpOperationResponseSchema.model_validate_json(response.text)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции кэшбэка.

        :param request: PyDantic модель BaseOperationRequestSchema,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request.model_dump(by_alias=True))

    def make_cashback_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                status: OperationStatus = OperationStatus.COMPLETED) -> MakeCashbackOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции кэшбэка.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeCashbackOperationResponseSchema
        """
        request = MakeCashbackOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_cashback_operation_api(request)
        return MakeCashbackOperationResponseSchema.model_validate_json(response.text)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции перевода.

        :param request: PyDantic модель BaseOperationRequestSchema,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request.model_dump(by_alias=True))

    def make_transfer_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                status: OperationStatus = OperationStatus.COMPLETED) -> MakeTransferOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции перевода.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakeTransferOperationResponseSchema
        """
        request = MakeTransferOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_transfer_operation_api(request)
        return MakeTransferOperationResponseSchema.model_validate_json(response.text)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции покупки.

        :param request: PyDantic модель BaseOperationRequestSchema,
                        дополненный полями category.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request.model_dump(by_alias=True))

    def make_purchase_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                status: OperationStatus = OperationStatus.COMPLETED,
                                category: str = "Learning") -> MakePurchaseOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции покупки.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :return: JSON -> MakePurchaseOperationResponseSchema
        """
        request = MakePurchaseOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_purchase_operation_api(request)
        return MakePurchaseOperationResponseSchema.model_validate_json(response.text)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции оплаты по счёту.

        :param request: PyDantic модель BaseOperationRequestSchema,
                        дополненный полями billId и provider.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request.model_dump(by_alias=True))

    def make_bill_payment_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                    status: OperationStatus = OperationStatus.COMPLETED) -> MakeBillPaymentOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции оплаты по счёту.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :param amount: float – Сумма операции. (например, 55.77)
        :param status: OperationStatus – Статус операции. (например, OperationStatus.COMPLETED)
        :return: JSON -> MakeBillPaymentOperationResponseSchema
        """
        request = MakeBillPaymentOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_bill_payment_operation_api(request)
        return MakeBillPaymentOperationResponseSchema.model_validate_json(response.text)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции снятия наличных.

        :param request: PyDantic модель BaseOperationRequestSchema,
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request.model_dump(by_alias=True))

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str, amount: float = 55.77,
                                       status: OperationStatus = OperationStatus.COMPLETED) -> MakeCashWithdrawalOperationResponseSchema:
        """
        WRAPPER: Выполняет POST-запрос для создания операции снятия наличных.
        :param card_id: str – Идентификатор карты. (например, "f29fd4dc-dc9a-45dd-9d85-d575317316ca")
        :param account_id: str – Идентификатор счёта. (например, "6bf8c921-7ce3-4a17-a201-96180a10842f")
        :param amount: float – Сумма операции. (например, 55.77)
        :param status: OperationStatus – Статус операции. (например, OperationStatus.COMPLETED)
        :return: JSON -> MakeCashWithdrawalOperationResponseSchema
        """
        request = MakeCashWithdrawalOperationRequestSchema(card_id=card_id, account_id=account_id)
        response = self.make_cash_withdrawal_operation_api(request)
        return MakeCashWithdrawalOperationResponseSchema.model_validate_json(response.text)


# Добавляем builder для OperationsGatewayHTTPClient – 7.5
def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию OperationsGatewayHTTPClient.
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
        # Генерация данных теперь происходит внутри схемы запроса
        create_user_request: CreateUserRequestSchema = CreateUserRequestSchema()
        create_user_resp = users_client.create_user_api(create_user_request)
        create_user_resp.raise_for_status()
        user_data = create_user_resp.json()
        user_id = user_data.get("id") or user_data.get("user", {}).get("id")
        print("*** Создан пользователь с ID:", user_id, "*** \n")
        print(JSONOutput.get_json(user_data))

        # 2. Открытие дебетового счёта/карты
        from clients.http.gateway.accounts.client import OpenDebitCardAccountRequestSchema

        open_debit_request: OpenDebitCardAccountRequestSchema = OpenDebitCardAccountRequestSchema(user_id=user_id)
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
        top_up_request: MakeTopUpOperationRequestSchema = MakeTopUpOperationRequestSchema(
            status=OperationStatus.COMPLETED,
            amount=1000.0,
            account_id=account_id,
            card_id=card_id
        )
        make_top_up_resp = operations_client.make_top_up_operation_api(top_up_request)
        make_top_up_resp.raise_for_status()
        top_up_data = make_top_up_resp.json()
        operation_id = top_up_data.get("operation", {}).get("id")
        print("*** Создана операция пополнения с ID:", operation_id, " *** \n")

        # 4. Чек по операции
        receipt_resp = operations_client.get_operation_receipt_api(
            GetOperationReceiptPathParamsSchema(operation_id=operation_id)
        )
        receipt_resp.raise_for_status()
        print("*** Чек по операции с ID:", operation_id, ": *** \n")
        print(receipt_resp.json())
