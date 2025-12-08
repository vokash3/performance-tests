# 7.2 Создание операции пополнения счёта

import time
import httpx
import faker

BASE_URL = "http://155.212.171.137:8003/api/v1"
KAFKA_MSG = "http://155.212.171.137:8081/ui/clusters/local-kafka/all-topics/documents-service.contracts.inbox/messages?keySerde=String&valueSerde=String&limit=100"
fake = faker.Faker("ru_RU")
enroll_amount = 1500


def enroll_payment():
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

    payload = {
        "userId": user_id,
    }

    print("\n*** Открытие дебетового счёта ***")
    resp = httpx.post(
        f"{BASE_URL}/accounts/open-debit-card-account",
        json=payload,
        timeout=5.0,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("Ответ JSON:", data)

    assert resp.status_code == 200, "Ошибка при открытии дебетового счёта"

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

    payload = {
        "status": "COMPLETED",
        "amount": enroll_amount,
        "cardId": card_id,
        "accountId": account_id,
    }

    print("\n*** Пополнение счёта ***")
    resp = httpx.post(
        f"{BASE_URL}/operations/make-top-up-operation",
        json=payload,
        timeout=5.0,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        data = {"error": "NO JSON!", "text": resp.text}
    print("Make top up operation response:", data)

    assert resp.status_code == 200, "Ошибка при выполнении операции пополнения"


if __name__ == "__main__":
    enroll_payment()
    print("=============================")
    print(f"Сообщения в Кафке – {KAFKA_MSG}")
