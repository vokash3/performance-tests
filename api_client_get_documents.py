from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.accounts.schema import OpenCreditCardAccountResponseSchema
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client
from helpers.json_output import JSONOutput

users_gateway_client = build_users_gateway_http_client()
cards_gateway_client = build_cards_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
documents_gateway_client = build_documents_gateway_http_client()

# Создаем пользователя
create_user_response = users_gateway_client.create_user()
print('Create user response:', create_user_response)

# Открываем кредитный счет
open_debit_card_account_response: OpenCreditCardAccountResponseSchema = accounts_gateway_client.open_credit_card_account(
    user_id=create_user_response.user.id,
)
print('Open credit card account response:', JSONOutput.get_json(open_debit_card_account_response))

# Получаем документ тарифа
tarif_document_response = documents_gateway_client.get_tariff_document(
    open_debit_card_account_response.account.id)
print('Get tariff document response:', JSONOutput.get_json(tarif_document_response))
