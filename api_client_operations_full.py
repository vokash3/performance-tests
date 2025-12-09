from typing import TypedDict

from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client
from helpers.json_output import JSONOutput


def print_step(title: str, payload):
    print(f"\n==== {title} ====\n")
    print(JSONOutput.get_json(payload))


def main():
    users_client = build_users_gateway_http_client()
    accounts_client = build_accounts_gateway_http_client()
    operations_client = build_operations_gateway_http_client()

    # 1. Пользователь
    user = users_client.create_user()
    print_step("Create user", user)
    user_id = user["user"]["id"]

    # 2. Дебетовый счёт/карта
    account = accounts_client.open_debit_card_account(user_id=user_id)
    print_step("Open debit card account", account)

    account_id = account["account"]["id"]
    cards = account["account"]["cards"]
    assert cards, "No cards returned for account"
    card_id = cards[0]["id"]

    #  Локальный хелпер для одной операции
    def run_operation(kind: str, op_response):
        print_step(f"{kind} operation", op_response)
        op_id = op_response["operation"]["id"]

        # get_operation
        op = operations_client.get_operation(op_id)
        print_step(f"Get {kind} operation", op)

        # get_operation_receipt
        receipt = operations_client.get_operation_receipt(op_id)
        print_step(f"{kind} operation receipt", receipt)

        return op_id

    # 3. Разные типы операций
    fee_op = operations_client.make_fee_operation(card_id=card_id, account_id=account_id)
    run_operation("Fee", fee_op)

    top_up_op = operations_client.make_top_up_operation(card_id=card_id, account_id=account_id)
    run_operation("Top up", top_up_op)

    cashback_op = operations_client.make_cashback_operation(card_id=card_id, account_id=account_id)
    run_operation("Cashback", cashback_op)

    transfer_op = operations_client.make_transfer_operation(card_id=card_id, account_id=account_id)
    run_operation("Transfer", transfer_op)

    purchase_op = operations_client.make_purchase_operation(card_id=card_id, account_id=account_id)
    run_operation("Purchase", purchase_op)

    bill_payment_op = operations_client.make_bill_payment_operation(card_id=card_id, account_id=account_id)
    run_operation("Bill payment", bill_payment_op)

    cash_withdrawal_op = operations_client.make_cash_withdrawal_operation(card_id=card_id, account_id=account_id)
    run_operation("Cash withdrawal", cash_withdrawal_op)

    # 4. Сводка по счёту
    operations_list = operations_client.get_operations(account_id=account_id)
    print_step("Get operations", operations_list)

    operations_summary = operations_client.get_operations_summary(account_id=account_id)
    print_step("Get operations summary", operations_summary)


if __name__ == "__main__":
    main()
