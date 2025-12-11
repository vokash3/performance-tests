from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client

from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import (
    OperationsGatewayServiceStub,
)

from contracts.services.gateway.operations.rpc_get_operation_pb2 import (
    GetOperationRequest,
    GetOperationResponse,
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest,
    GetOperationReceiptResponse,
)
from contracts.services.gateway.operations.rpc_get_operations_pb2 import (
    GetOperationsRequest,
    GetOperationsResponse,
)
from contracts.services.gateway.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse,
)

from contracts.services.gateway.operations.rpc_make_fee_operation_pb2 import (
    MakeFeeOperationRequest,
    MakeFeeOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import (
    MakeTopUpOperationRequest,
    MakeTopUpOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_cashback_operation_pb2 import (
    MakeCashbackOperationRequest,
    MakeCashbackOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_transfer_operation_pb2 import (
    MakeTransferOperationRequest,
    MakeTransferOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_purchase_operation_pb2 import (
    MakePurchaseOperationRequest,
    MakePurchaseOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_bill_payment_operation_pb2 import (
    MakeBillPaymentOperationRequest,
    MakeBillPaymentOperationResponse,
)
from contracts.services.gateway.operations.rpc_make_cash_withdrawal_operation_pb2 import (
    MakeCashWithdrawalOperationRequest,
    MakeCashWithdrawalOperationResponse,
)

from contracts.services.operations.operation_pb2 import OperationStatus
from tools.fakers import fake


class OperationsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с OperationsGatewayService.

    Предоставляет низкоуровневые и высокоуровневые методы
    для получения информации об операциях и создания различных типов операций.
    """

    def __init__(self, channel: Channel) -> None:
        """
        Инициализирует клиента с указанным gRPC-каналом.

        :param channel: gRPC-канал для подключения к OperationsGatewayService.
        """
        super().__init__(channel)
        self.stub = OperationsGatewayServiceStub(channel)
        self.op_status = fake.proto_enum(OperationStatus)

    # -------- Низкоуровневые методы (API) --------

    def get_operation_api(self, request: GetOperationRequest) -> GetOperationResponse:
        """
        Низкоуровневый вызов метода GetOperation через gRPC.

        :param request: gRPC-запрос с идентификатором операции.
        :return: Ответ сервиса с данными операции.
        """
        return self.stub.GetOperation(request)

    def get_operation_receipt_api(
            self,
            request: GetOperationReceiptRequest,
    ) -> GetOperationReceiptResponse:
        """
        Низкоуровневый вызов метода GetOperationReceipt через gRPC.

        :param request: gRPC-запрос с идентификатором операции.
        :return: Ответ сервиса с данными чека по операции.
        """
        return self.stub.GetOperationReceipt(request)

    def get_operations_api(self, request: GetOperationsRequest) -> GetOperationsResponse:
        """
        Низкоуровневый вызов метода GetOperations через gRPC.

        :param request: gRPC-запрос с идентификатором счёта.
        :return: Ответ сервиса со списком операций по счёту.
        """
        return self.stub.GetOperations(request)

    def get_operations_summary_api(
            self,
            request: GetOperationsSummaryRequest,
    ) -> GetOperationsSummaryResponse:
        """
        Низкоуровневый вызов метода GetOperationsSummary через gRPC.

        :param request: gRPC-запрос с идентификатором счёта.
        :return: Ответ сервиса со сводной статистикой по операциям счёта.
        """
        return self.stub.GetOperationsSummary(request)

    def make_fee_operation_api(
            self,
            request: MakeFeeOperationRequest,
    ) -> MakeFeeOperationResponse:
        """
        Низкоуровневый вызов метода MakeFeeOperation через gRPC.

        :param request: gRPC-запрос на создание операции комиссии.
        :return: Ответ сервиса с данными созданной операции комиссии.
        """
        return self.stub.MakeFeeOperation(request)

    def make_top_up_operation_api(
            self,
            request: MakeTopUpOperationRequest,
    ) -> MakeTopUpOperationResponse:
        """
        Низкоуровневый вызов метода MakeTopUpOperation через gRPC.

        :param request: gRPC-запрос на создание операции пополнения.
        :return: Ответ сервиса с данными созданной операции пополнения.
        """
        return self.stub.MakeTopUpOperation(request)

    def make_cashback_operation_api(
            self,
            request: MakeCashbackOperationRequest,
    ) -> MakeCashbackOperationResponse:
        """
        Низкоуровневый вызов метода MakeCashbackOperation через gRPC.

        :param request: gRPC-запрос на создание операции кэшбэка.
        :return: Ответ сервиса с данными созданной операции кэшбэка.
        """
        return self.stub.MakeCashbackOperation(request)

    def make_transfer_operation_api(
            self,
            request: MakeTransferOperationRequest,
    ) -> MakeTransferOperationResponse:
        """
        Низкоуровневый вызов метода MakeTransferOperation через gRPC.

        :param request: gRPC-запрос на создание операции перевода.
        :return: Ответ сервиса с данными созданной операции перевода.
        """
        return self.stub.MakeTransferOperation(request)

    def make_purchase_operation_api(
            self,
            request: MakePurchaseOperationRequest,
    ) -> MakePurchaseOperationResponse:
        """
        Низкоуровневый вызов метода MakePurchaseOperation через gRPC.

        :param request: gRPC-запрос на создание операции покупки.
        :return: Ответ сервиса с данными созданной операции покупки.
        """
        return self.stub.MakePurchaseOperation(request)

    def make_bill_payment_operation_api(
            self,
            request: MakeBillPaymentOperationRequest,
    ) -> MakeBillPaymentOperationResponse:
        """
        Низкоуровневый вызов метода MakeBillPaymentOperation через gRPC.

        :param request: gRPC-запрос на создание операции оплаты по счёту.
        :return: Ответ сервиса с данными созданной операции оплаты по счёту.
        """
        return self.stub.MakeBillPaymentOperation(request)

    def make_cash_withdrawal_operation_api(
            self,
            request: MakeCashWithdrawalOperationRequest,
    ) -> MakeCashWithdrawalOperationResponse:
        """
        Низкоуровневый вызов метода MakeCashWithdrawalOperation через gRPC.

        :param request: gRPC-запрос на создание операции снятия наличных.
        :return: Ответ сервиса с данными созданной операции снятия наличных.
        """
        return self.stub.MakeCashWithdrawalOperation(request)

    # -------- Высокоуровневые методы (обёртки) --------

    def get_operation(self, operation_id: str) -> GetOperationResponse:
        """
        Получение информации об операции по её идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Ответ с данными операции.
        """
        request = GetOperationRequest(id=operation_id)
        return self.get_operation_api(request)

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponse:
        """
        Получение чека по операции.

        :param operation_id: Идентификатор операции.
        :return: Ответ с данными чека по операции.
        """
        request = GetOperationReceiptRequest(operation_id=operation_id)
        return self.get_operation_receipt_api(request)

    def get_operations(self, account_id: str) -> GetOperationsResponse:
        """
        Получение списка операций по счёту.

        :param account_id: Идентификатор счёта.
        :return: Ответ со списком операций по счёту.
        """
        request = GetOperationsRequest(account_id=account_id)
        return self.get_operations_api(request)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponse:
        """
        Получение сводной информации по операциям счёта.

        :param account_id: Идентификатор счёта.
        :return: Ответ со статистикой по операциям.
        """
        request = GetOperationsSummaryRequest(account_id=account_id)
        return self.get_operations_summary_api(request)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponse:
        """
        Создание операции комиссии для указанной карты и счёта.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции комиссии.
        """
        request = MakeFeeOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_fee_operation_api(request)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponse:
        """
        Создание операции пополнения счёта.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции пополнения.
        """
        request = MakeTopUpOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_top_up_operation_api(request)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponse:
        """
        Создание операции кэшбэка.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции кэшбэка.
        """
        request = MakeCashbackOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_cashback_operation_api(request)

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponse:
        """
        Создание операции перевода.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции перевода.
        """
        request = MakeTransferOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_transfer_operation_api(request)

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponse:
        """
        Создание операции покупки.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции покупки.
        """
        request = MakePurchaseOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            category=fake.category(),
            account_id=account_id,
        )
        return self.make_purchase_operation_api(request)

    def make_bill_payment_operation(
            self,
            card_id: str,
            account_id: str,
    ) -> MakeBillPaymentOperationResponse:
        """
        Создание операции оплаты по счёту.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции оплаты по счёту.
        """
        request = MakeBillPaymentOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_bill_payment_operation_api(request)

    def make_cash_withdrawal_operation(
            self,
            card_id: str,
            account_id: str,
    ) -> MakeCashWithdrawalOperationResponse:
        """
        Создание операции снятия наличных.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счёта.
        :return: Ответ с данными созданной операции снятия наличных.
        """
        request = MakeCashWithdrawalOperationRequest(
            status=self.op_status,
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id,
        )
        return self.make_cash_withdrawal_operation_api(request)


def build_operations_gateway_grpc_client() -> OperationsGatewayGRPCClient:
    """
    Фабрика для создания экземпляра OperationsGatewayGRPCClient.

    :return: Инициализированный клиент для OperationsGatewayService.
    """
    return OperationsGatewayGRPCClient(channel=build_gateway_grpc_client())


def main():
    """
    Тестовый сценарий:
        - создаёт пользователя
        - открывает дебетовый счёт
        - выпускает виртуальную карту (если её ещё нет)
        - вызывает все make_* операции
        - запрашивает операции, сводку, отдельную операцию и чек
    (!) Можем столкнуться с проблемой, если СТАТУС ОТЛИЧЕН ОТ
    status: OPERATION_STATUS_IN_PROGRESS (1) или OPERATION_STATUS_COMPLETED (2):
        grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.INTERNAL
        details = "Get receipt: An error occurred (NoSuchKey) when calling the GetObject operation:
        The specified key does not exist."
        debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:13, grpc_message:"Get receipt:
        An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist."}"

    Для справки:
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        OPERATION_STATUS_UNSPECIFIED: _OperationStatus.ValueType  # 0
        OPERATION_STATUS_IN_PROGRESS: _OperationStatus.ValueType  # 1
        OPERATION_STATUS_COMPLETED: _OperationStatus.ValueType  # 2
        OPERATION_STATUS_FAILED: _OperationStatus.ValueType  # 3
    """
    from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
    from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
    from clients.grpc.gateway.cards.client import build_cards_gateway_grpc_client
    users_client = build_users_gateway_grpc_client()
    accounts_client = build_accounts_gateway_grpc_client()
    cards_client = build_cards_gateway_grpc_client()
    operations_client = build_operations_gateway_grpc_client()

    print("STATUS для операций: ", operations_client.op_status)
    print("==============================================")

    # 1. Пользователь
    user_resp = users_client.create_user()
    user = user_resp.user
    print("Create user response:", user_resp)

    # 2. Дебетовый счёт
    debit_resp = accounts_client.open_debit_card_account(user_id=user.id)
    account = debit_resp.account
    print("Open debit account response:", debit_resp)

    # 3. Карта
    if account.cards:
        card = account.cards[0]
        print("Using existing card from account:", card)
    else:
        card_resp = cards_client.issue_virtual_card(user_id=user.id, account_id=account.id)
        card = card_resp.card
        print("Issue virtual card response:", card_resp)

    card_id = card.id
    account_id = account.id

    # 4. Все операции make_* (сохраняем operation_id последней — по ней возьмём чек)
    fee_resp = operations_client.make_fee_operation(card_id=card_id, account_id=account_id)
    print("Make fee operation response:", fee_resp)

    top_up_resp = operations_client.make_top_up_operation(card_id=card_id, account_id=account_id)
    print("Make top up operation response:", top_up_resp)

    cashback_resp = operations_client.make_cashback_operation(card_id=card_id, account_id=account_id)
    print("Make cashback operation response:", cashback_resp)

    transfer_resp = operations_client.make_transfer_operation(card_id=card_id, account_id=account_id)
    print("Make transfer operation response:", transfer_resp)

    purchase_resp = operations_client.make_purchase_operation(card_id=card_id, account_id=account_id)
    print("Make purchase operation response:", purchase_resp)

    bill_payment_resp = operations_client.make_bill_payment_operation(card_id=card_id, account_id=account_id)
    print("Make bill payment operation response:", bill_payment_resp)

    cash_withdrawal_resp = operations_client.make_cash_withdrawal_operation(card_id=card_id, account_id=account_id)
    print("Make cash withdrawal operation response:", cash_withdrawal_resp)

    # Будем использовать последнюю операцию для get_operation / receipt
    operation = cash_withdrawal_resp.operation

    # 5. GetOperations и GetOperationsSummary по счёту
    operations_list_resp = operations_client.get_operations(account_id=account_id)
    print("Get operations response:", operations_list_resp)

    operations_summary_resp = operations_client.get_operations_summary(account_id=account_id)
    print("Get operations summary response:", operations_summary_resp)

    # 6. GetOperation по конкретной операции
    get_op_resp = operations_client.get_operation(operation_id=operation.id)
    print("Get operation response:", get_op_resp)

    # 7. GetOperationReceipt по этой же операции
    receipt_resp = operations_client.get_operation_receipt(operation_id=operation.id)
    print("Get operation receipt response:", receipt_resp)


if __name__ == '__main__':
    """
    Для теста клиента.
    """
    main()
