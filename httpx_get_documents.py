# 7.2 Получение документов по счёту – создание кредитного счёта

import time
import httpx
import faker

BASE_URL = "http://155.212.171.137:8003/api/v1"
KAFKA_MSG = "http://155.212.171.137:8081/ui/clusters/local-kafka/all-topics/documents-service.contracts.inbox/messages?keySerde=String&valueSerde=String&limit=100"
fake = faker.Faker("ru_RU")


def open_credit_account():
    """
    Открытие кредитного счёта
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

    print("\n*** Открытие кредитного счёта ***")
    resp_post_open_credit_card_account = httpx.post(
        f"{BASE_URL}/accounts/open-credit-card-account",
        json=open_debit_card_account_payload,
        timeout=5.0,
    )
    print("Status:", resp_post_open_credit_card_account.status_code)
    assert resp_post_create_user.status_code == 200, "Ошибка при открытии кредитного счёта"
    try:
        open_credit_card_json = resp_post_open_credit_card_account.json()
    except ValueError:
        open_credit_card_json = {"error": "NO JSON!", "text": resp_post_open_credit_card_account.text}
    print("Ответ JSON:", open_credit_card_json)

    print("*** Получаем тарифный документ ***")
    account_id = open_credit_card_json.get("account", {}).get("id")
    if not user_id:
        raise RuntimeError("Не удалось вытащить account.id из ответа")

    resp_get_tariff_document_response = httpx.get(f"{BASE_URL}/documents/tariff-document/{account_id}")
    assert resp_get_tariff_document_response.status_code == 200, "Ошибка при получении тарифного документа"
    tariff_document_json = resp_get_tariff_document_response.json()

    print("Get tariff document response:", tariff_document_json)
    print("Get tariff document status code:", resp_get_tariff_document_response.status_code)

    print("*** Получаем контракт ***")
    resp_get_contract_document = httpx.get(f"{BASE_URL}/documents/contract-document/{account_id}")
    assert resp_get_contract_document.status_code == 200, "Ошибка при получении контракта"
    contract_document_json = resp_get_contract_document.json()
    print("Get contract document response:", contract_document_json)
    print("Get contract document status code:", resp_get_contract_document.status_code)


if __name__ == "__main__":
    open_credit_account()
    print("=============================")
    print(f"Сообщения в Кафке – {KAFKA_MSG}")
