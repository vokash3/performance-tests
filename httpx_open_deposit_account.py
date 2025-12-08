import time
import httpx
import faker

BASE_URL = "http://155.212.171.137:8003/api/v1"
KAFKA_MSG = "http://155.212.171.137:8081/ui/clusters/local-kafka/all-topics/documents-service.contracts.inbox/messages?keySerde=String&valueSerde=String&limit=100"
fake = faker.Faker("ru_RU")


def open_deposit_account():
    """
    Открытие депозитного счёта
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

    open_deposit_payload = {
        "user_id": user_id,
    }

    resp_post_open_deposit = httpx.post(
        f"{BASE_URL}/accounts/open-deposit-account",
        json=open_deposit_payload,
        timeout=5.0,
    )

    print("\n*** Открытие депозитного счёта ***")
    print("Status:", resp_post_open_deposit.status_code)
    assert resp_post_open_deposit.status_code == 200, "Ошибка при открытии депозитного счёта"
    try:
        deposit_json = resp_post_open_deposit.json()
    except ValueError:
        deposit_json = {"error": "NO JSON!", "text": resp_post_open_deposit.text}
    print("Ответ JSON:", deposit_json)
    print("=============================")
    print(f"Сообщения в Кафке – {KAFKA_MSG}")


if __name__ == "__main__":
    open_deposit_account()
