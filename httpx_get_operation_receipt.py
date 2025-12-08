# 7.2 Получение чека по операции

import time
import httpx
import faker

BASE_URL = "http://155.212.171.137:8003/api/v1"
KAFKA_MSG = "http://155.212.171.137:8081/ui/clusters/local-kafka/all-topics/documents-service.contracts.inbox/messages?keySerde=String&valueSerde=String&limit=100"
fake = faker.Faker("ru_RU")


def create_user() -> dict:
    """
    Создание пользователя /api/v1/users
    """
    unique_email = f"user_{time.time()}@example.com"
    payload = {
        "email": unique_email,
        "lastName": fake.last_name_male(),
        "firstName": fake.first_name_male(),
        "middleName": fake.middle_name_male(),
        "phoneNumber": fake.phone_number(),
    }

    resp = httpx.post(f"{BASE_URL}/users", json=payload, timeout=5.0)

    print("*** Создание пользователя ***")
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("JSON:", data)

    assert resp.status_code == 200, "Ошибка при создании пользователя"

    user_id = data.get("id") or data.get("user", {}).get("id")
    if not user_id:
        raise RuntimeError("Не удалось вытащить user.id из ответа")

    return {"user_id": user_id, "raw": data}


def open_credit_account(user_id: int | str) -> dict:
    """
    Открытие кредитного счёта (с картой) /api/v1/accounts/open-credit-card-account
    """
    payload = {
        "userId": user_id,
    }

    print("\n*** Открытие кредитного счёта ***")
    resp = httpx.post(
        f"{BASE_URL}/accounts/open-credit-card-account",
        json=payload,
        timeout=5.0,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("Ответ JSON:", data)

    assert resp.status_code == 200, "Ошибка при открытии кредитного счёта"

    account = data.get("account") or {}
    account_id = account.get("id")
    cards = account.get("cards") or []
    if not account_id:
        raise RuntimeError("Не удалось вытащить account.id из ответа")
    if not cards:
        raise RuntimeError("Не удалось вытащить cards[0].id из ответа")

    card_id = cards[0].get("id")
    if not card_id:
        raise RuntimeError("Не удалось вытащить card.id из ответа")

    return {
        "account_id": account_id,
        "card_id": card_id,
        "raw": data,
    }


def make_purchase_operation(
        account_id: int | str,
        card_id: int | str,
        amount: float = 77.99,
        category: str = "taxi",
) -> dict:
    """
    Совершение операции покупки (purchase) /api/v1/operations/make-purchase-operation
    """
    payload = {
        "status": "IN_PROGRESS",
        "amount": amount,
        "category": category,
        "cardId": card_id,
        "accountId": account_id,
    }

    print("\n*** Операция покупки (purchase) ***")
    resp = httpx.post(
        f"{BASE_URL}/operations/make-purchase-operation",
        json=payload,
        timeout=5.0,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("Purchase operation response:", data)

    assert resp.status_code == 200, "Ошибка при выполнении операции покупки"

    operation_id = data.get("id") or data.get("operation", {}).get("id")
    if not operation_id:
        raise RuntimeError("Не удалось вытащить operation.id из ответа")

    return {
        "operation_id": operation_id,
        "raw": data,
    }


def get_operation_receipt(operation_id: int | str) -> dict:
    """
    Получение чека по операции /api/v1/operations/operation-receipt/{operation_id}
    """
    print("\n*** Получение чека по операции ***")
    resp = httpx.get(
        f"{BASE_URL}/operations/operation-receipt/{operation_id}",
        timeout=5.0,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("Operation receipt JSON:", data)

    assert resp.status_code == 200, "Ошибка при получении чека по операции"

    return data


def main():
    user = create_user()
    credit = open_credit_account(user["user_id"])
    purchase = make_purchase_operation(
        account_id=credit["account_id"],
        card_id=credit["card_id"],
        amount=77.99,
        category="taxi",
    )
    get_operation_receipt(purchase["operation_id"])
    print("=============================")
    print(f"Сообщения в Кафке – {KAFKA_MSG}")


if __name__ == "__main__":
    main()
