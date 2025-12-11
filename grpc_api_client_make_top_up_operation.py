"""
Тестовый сценарий:
    – Создаёт пользователя.
    – Открывает дебетовый счёт для этого пользователя..
    – Создает операцию пополнение дебетового счета.
"""
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client

users_client = build_users_gateway_grpc_client()
accounts_client = build_accounts_gateway_grpc_client()
operations_client = build_operations_gateway_grpc_client()

# 1. Пользователь
user_resp = users_client.create_user()
user = user_resp.user
print("Create user response:", user_resp)

# 2. Дебетовый счёт
account_debit_resp = accounts_client.open_debit_card_account(user.id)
account = account_debit_resp.account
card = account_debit_resp.account.cards[0]
print("Open credit account response:", account_debit_resp)

# 3. Операция пополнения
op_top_up_resp = operations_client.make_top_up_operation(card.id, account.id)
print("Operation make top up response:", op_top_up_resp)
