import grpc

# gRPC-клиенты для соответствующих сервисов
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse,
)
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import (
    MakeTopUpOperationRequest,
    MakeTopUpOperationResponse,
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest,
    GetOperationReceiptResponse,
)
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub

# Enum со статусами операций
from contracts.services.operations.operation_pb2 import OperationStatus

# Фейковые данные для тестов
from tools.fakers import fake


def main() -> None:
    # Создаём gRPC-канал к сервисам, работающим на порту 9003
    channel = grpc.insecure_channel("155.212.171.137:9003")

    # Инициализируем stubs (gRPC-клиенты)
    users_gateway_service = UsersGatewayServiceStub(channel)
    accounts_gateway_service = AccountsGatewayServiceStub(channel)
    operations_gateway_service = OperationsGatewayServiceStub(channel)

    # 1. Создаём нового пользователя
    create_user_request = CreateUserRequest(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        middle_name=fake.middle_name(),
        phone_number=fake.phone_number(),
    )
    create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)
    print("Create user response:", create_user_response)

    # 2. Открываем дебетовый счёт на созданного пользователя
    open_debit_card_account_request = OpenDebitCardAccountRequest(
        user_id=create_user_response.user.id,
    )
    open_debit_card_account_response: OpenDebitCardAccountResponse = (
        accounts_gateway_service.OpenDebitCardAccount(open_debit_card_account_request)
    )
    print("Open debit card account response:", open_debit_card_account_response)

    # Достаём нужные идентификаторы
    account_id = open_debit_card_account_response.account.id
    card_id = open_debit_card_account_response.account.cards[0].id

    # 3. Выполняем операцию пополнения счёта
    make_top_up_operation_request = MakeTopUpOperationRequest(
        status=OperationStatus.OPERATION_STATUS_COMPLETED,  # Статус операции — завершена
        amount=fake.amount(),  # Сумма пополнения
        card_id=card_id,  # ID первой карты счёта
        account_id=account_id,  # ID счёта
    )
    make_top_up_operation_response: MakeTopUpOperationResponse = operations_gateway_service.MakeTopUpOperation(
        make_top_up_operation_request
    )
    print("Make top up operation response:", make_top_up_operation_response)

    # ID операции для получения чека
    operation_id = make_top_up_operation_response.operation.id

    # 4. Получаем чек по операции
    get_operation_receipt_request = GetOperationReceiptRequest(
        operation_id=operation_id,
    )
    get_operation_receipt_response: GetOperationReceiptResponse = operations_gateway_service.GetOperationReceipt(
        get_operation_receipt_request
    )
    print('Get operation receipt response:', get_operation_receipt_response)


if __name__ == "__main__":
    main()
