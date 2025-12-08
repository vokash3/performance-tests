# 7.2 Выпуск виртуальной карты

import time
import httpx
import faker

BASE_URL = "http://155.212.171.137:8003/api/v1"
KAFKA_MSG = "http://155.212.171.137:8081/ui/clusters/local-kafka/all-topics/documents-service.contracts.inbox/messages?keySerde=String&valueSerde=String&limit=100"
fake = faker.Faker("ru_RU")


def open_debit_account():
    """
    Открытие дебетового счёта
    Контракт – http://155.212.171.137:8003/docs
    :return:
    """
    unique_email = f"user_{time.time()}@example.com"
    create_user_payload = {
        "email": unique_email,
        "lastName": fake.last_name_male(),
        "firstName": fake.first_name_male(),
        "middleName": fake.middle_name_male(),
        "phoneNumber": fake.phone_number(),
    }

    resp_post_create_user = httpx.post(
        f"{BASE_URL}/users",
        json=create_user_payload,
        timeout=5.0,
    )

    print("*** Создание пользователя ***")
    print("Status:", resp_post_create_user.status_code)
    assert resp_post_create_user.status_code == 200, "Ошибка при создании пользователя"
    try:
        user_json = resp_post_create_user.json()
    except ValueError:
        user_json = {"error": "NO JSON!", "text": resp_post_create_user.text}
    print("JSON:", user_json)

    user_id = user_json.get("id") or user_json.get("user", {}).get("id")
    if not user_id:
        raise RuntimeError("Не удалось вытащить user.id из ответа")

    open_debit_card_account_payload = {
        "userId": user_id,
    }

    print("\n*** Открытие дебетового счёта ***")
    resp_post_open_debit_card_account = httpx.post(
        f"{BASE_URL}/accounts/open-debit-card-account",
        json=open_debit_card_account_payload,
        timeout=5.0,
    )
    print("Status:", resp_post_open_debit_card_account.status_code)
    assert resp_post_create_user.status_code == 200, "Ошибка при открытии дебетового счёта"
    try:
        open_debit_json = resp_post_open_debit_card_account.json()
    except ValueError:
        open_debit_json = {"error": "NO JSON!", "text": resp_post_open_debit_card_account.text}
    print("Ответ JSON:", open_debit_json)

    print("*** Выпуск виртуальной карты ***")
    account_id = open_debit_json.get("account", {}).get("id")
    if not user_id:
        raise RuntimeError("Не удалось вытащить account.id из ответа")

    issue_virtual_card_payload = {
        "userId": user_id,
        "accountId": account_id,
    }
    resp_post_issue_virtual_card_response = httpx.post(
        f"{BASE_URL}/cards/issue-virtual-card",
        json=issue_virtual_card_payload
    )
    issue_virtual_card_response_data = resp_post_issue_virtual_card_response.json()

    # Выводим результат
    print("Issue virtual card response:", issue_virtual_card_response_data)
    print("Issue virtual card status code:", resp_post_issue_virtual_card_response.status_code)


if __name__ == "__main__":
    open_debit_account()
    print("=============================")
    print(f"Сообщения в Кафке – {KAFKA_MSG}")
