import grpc

from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub

from tools.fakers import fake  # Используем генератор фейковых данных, созданный ранее

# Устанавливаем соединение с gRPC-сервером по адресу localhost:9003
channel = grpc.insecure_channel("155.212.171.137:9003")

# Создаём gRPC-клиент для UsersGatewayService
users_gateway_service = UsersGatewayServiceStub(channel)
# Создаём gRPC-клиент для AccountsGatewayService
accounts_gateway_service = AccountsGatewayServiceStub(channel)

# Формируем запрос на создание пользователя с рандомными данными
create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)

# Отправляем запрос и получаем ответ
create_user_response: CreateUserResponse = users_gateway_service.CreateUser(create_user_request)
print('Create user response:', create_user_response)

# Формируем запрос на открытие дебетовой карты
open_debit_card_account_request = OpenDebitCardAccountRequest(user_id=create_user_response.user.id)
# Отправляем запрос и получаем ответ
open_debit_card_account_response = accounts_gateway_service.OpenDebitCardAccount(open_debit_card_account_request)
print('Get debit card account response:', open_debit_card_account_response)
