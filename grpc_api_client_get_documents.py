"""
Тестовый сценарий:
    – Создаёт пользователя.
    – Открывает кредитный счёт для этого пользователя.
    – Получает документ тарифа.
    – Получает документ контракта.
"""
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.cards.client import build_cards_gateway_grpc_client
from clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client

users_client = build_users_gateway_grpc_client()
accounts_client = build_accounts_gateway_grpc_client()
cards_client = build_cards_gateway_grpc_client()
operations_client = build_operations_gateway_grpc_client()
documents_client = build_documents_gateway_grpc_client()

# 1. Пользователь
user_resp = users_client.create_user()
user = user_resp.user
print("Create user response:", user_resp)

# 2. Крединтый счёт
card_credit_resp = accounts_client.open_credit_card_account(user_id=user.id)
account = card_credit_resp.account
print("Open credit account response:", card_credit_resp)

# 3. Документ тарифа
doc_tariff_resp = documents_client.get_tariff_document(card_credit_resp.account.id)
print("Tariff document response:", doc_tariff_resp)

# 4. Документ контракта
doc_contract_resp = documents_client.get_contract_document(card_credit_resp.account.id)
print("Get contract document response:", doc_contract_resp)
