# QA Performance Engineer

<img src="https://cdn.stepik.net/media/cache/images/courses/242935/cover_cE4uVIf/46ed8cc5a9b8982bd8e91ff34374a376.png" alt="Course cover" height="230" width="230">

Проект для взаимодействие с тестовой банковской системой в
рамках [курса Никиты Филонова на Stepik](https://stepik.org/242935).

_Проверено на Python3.12._

__Отдельный тестовый стенд развёрнут на виртуальном сервере.__

### Ссылки

- [OpenAPI](http://155.212.171.137:8003/docs)
- [pgAdmin](http://155.212.171.137:5050/)
- [Grafana](http://155.212.171.137:3002/d/23673d3b-5bd8-4027-88e4-31eb65880e72/docker-and-system-monitoring/)
- [MinIO](http://155.212.171.137:3001/)
- [Kafka](http://155.212.171.137:8081/)

---

# Подготовка к запуску

Работаем в рабочей директории **performance-tests**

- Создаём среду
  ```bash
  python3 -m venv venv
  ```
- Активируем venv
  ```bash
  source venv/bin/activate
  ```
- Устанавливаем зависимости
  ```bash
  pip install -r requirements.txt
  ```

---

## Task 7.1 – Создание депозитного счёта

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **httpx_open_deposit_account.py**
  ```bash
  python httpx_open_deposit_account.py
  ```

    - ### Пример успешного выполнения:
      ```
      *** Создание пользователя ***
      Status: 200
      JSON: {'user': {'id': '9edf45d7-4696-42c6-905d-7caf17ed38a6', 'email': 'user_1765232086.9166021@example.com', 'lastName': 'Фомичев', 'firstName': 'Амос', 'middleName': 'Авдеевич', 'phoneNumber': '85378155120'}}
    
      *** Открытие депозитного счёта ***
      Status: 200
      Ответ JSON: {'account': {'id': 'f891d448-aa49-4770-bb37-d394ab39aff5', 'type': 'DEPOSIT', 'cards': [], 'status': 'ACTIVE', 'balance': 0.0}}
      ```

---

## Task 7.2 – Получение чека по операции

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **httpx_open_deposit_account.py**
  ```bash
  python httpx_get_operation_receipt.py
  ```

    - ### Пример успешного выполнения:
      ```
      *** Создание пользователя ***
      Status: 200
      JSON: {'user': {'id': '06808055-dbf0-49d7-bab3-014aa01f8a73', 'email': 'user_1765233854.488649@example.com', 'lastName': 'Блинов', 'firstName': 'Елизар', 'middleName': 'Юльевич', 'phoneNumber': '83792740403'}}
    
      *** Открытие кредитного счёта ***
      Status: 200
      Ответ JSON: {'account': {'id': '1cd2a61b-0edc-401a-82ad-c5e693e9658f', 'type': 'CREDIT_CARD', 'cards': [{'id': '9e65b1d8-93ca-4788-b382-38cc3b2db603', 'pin': '2051', 'cvv': '796', 'type': 'VIRTUAL', 'status': 'ACTIVE', 'accountId': '1cd2a61b-0edc-401a-82ad-c5e693e9658f', 'cardNumber': '3512688786078052', 'cardHolder': 'Елизар Блинов', 'expiryDate': '2032-12-06', 'paymentSystem': 'MASTERCARD'}, {'id': '4a29fcbc-ba68-4a12-82d0-4d3a5bd70964', 'pin': '3391', 'cvv': '676', 'type': 'PHYSICAL', 'status': 'ACTIVE', 'accountId': '1cd2a61b-0edc-401a-82ad-c5e693e9658f', 'cardNumber': '3562656672529776', 'cardHolder': 'Елизар Блинов', 'expiryDate': '2032-12-06', 'paymentSystem': 'MASTERCARD'}], 'status': 'ACTIVE', 'balance': 25000.0}}
    
      *** Операция покупки (purchase) ***
      Status: 200
      Purchase operation response: {'operation': {'id': '3b5c74d5-d552-44af-9a39-134db4b83ccb', 'type': 'PURCHASE', 'status': 'IN_PROGRESS', 'amount': -77.99, 'cardId': '9e65b1d8-93ca-4788-b382-38cc3b2db603', 'category': 'taxi', 'createdAt': '2025-12-08T22:44:15.014317', 'accountId': '1cd2a61b-0edc-401a-82ad-c5e693e9658f'}}
    
      *** Получение чека по операции ***
      Status: 200
      Operation receipt JSON: {'receipt': {'url': 'http://localhost:3000/documents/receipt_3b5c74d5-d552-44af-9a39-134db4b83ccb.pdf', 'document': '3b5c74d5-d552-44af-9a39-134db4b83ccb'}}
      ```

---

## Task 7.3 – Написание HTTP API клиента (Cards)

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **clients/http/gateway/cards/client.py**
  ```bash
  PYTHONPATH=`pwd` python clients/http/gateway/cards/client.py
  ```

    - ### Пример успешного выполнения:
      ```
      VIRTUAL CARD: {
          "card": {
              "accountId": "c4d14cc2-6764-4305-b7f1-1f643072e4d4",
              "cardHolder": "Аникей Андреев",
              "cardNumber": "4425447716957",
              "cvv": "968",
              "expiryDate": "2032-12-07",
              "id": "144ffc92-8795-46c8-bb60-ce1e85e20fcd",
              "paymentSystem": "MASTERCARD",
              "pin": "2047",
              "status": "ACTIVE",
              "type": "VIRTUAL"
          }
      }
      
      PHYSICAL_CARD: {
          "card": {
              "accountId": "c4d14cc2-6764-4305-b7f1-1f643072e4d4",
              "cardHolder": "Аникей Андреев",
              "cardNumber": "180015439239617",
              "cvv": "174",
              "expiryDate": "2032-12-07",
              "id": "b44fc530-18a0-45b2-b637-6c3d7d33e9b1",
              "paymentSystem": "MASTERCARD",
              "pin": "8553",
              "status": "ACTIVE",
              "type": "PHYSICAL"
          }
      }
      ```

---

## Task 7.4 – Реализация HTTP API клиентов (Operations)

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **clients/http/gateway/operations/client.py**
  ```bash
  PYTHONPATH=`pwd` python clients/http/gateway/operations/client.py
  ```

    - ### Пример успешного выполнения:
      ```
        *** Создан пользователь с ID: 5a7f45c0-959f-45f5-91ed-8a393f9d7222 *** 
        
        {
            "user": {
                "email": "user_1765262656.894612@example.com",
                "firstName": "Ладимир",
                "id": "5a7f45c0-959f-45f5-91ed-8a393f9d7222",
                "lastName": "Ильин",
                "middleName": "Яковлевич",
                "phoneNumber": "+7 773 547 7054"
            }
        }
        *** Открыт дебетовый счёт с ID: 61587524-3f9a-4f84-a195-478926e2c572 и карта с ID: a6ee6467-5828-4e37-aeca-fbfc0ad51a9c *** 
        
        {
            "account": {
                "balance": 0.0,
                "cards": [
                    {
                        "accountId": "61587524-3f9a-4f84-a195-478926e2c572",
                        "cardHolder": "Ладимир Ильин",
                        "cardNumber": "6011301854671035",
                        "cvv": "615",
                        "expiryDate": "2032-12-07",
                        "id": "a6ee6467-5828-4e37-aeca-fbfc0ad51a9c",
                        "paymentSystem": "MASTERCARD",
                        "pin": "2213",
                        "status": "ACTIVE",
                        "type": "VIRTUAL"
                    },
                    {
                        "accountId": "61587524-3f9a-4f84-a195-478926e2c572",
                        "cardHolder": "Ладимир Ильин",
                        "cardNumber": "5180264237211852",
                        "cvv": "560",
                        "expiryDate": "2032-12-07",
                        "id": "51b17a80-6a93-4183-a9f0-2fba1cc92ca1",
                        "paymentSystem": "MASTERCARD",
                        "pin": "5716",
                        "status": "ACTIVE",
                        "type": "PHYSICAL"
                    }
                ],
                "id": "61587524-3f9a-4f84-a195-478926e2c572",
                "status": "ACTIVE",
                "type": "DEBIT_CARD"
            }
        }
        *** Создана операция пополнения с ID: 7f7aead2-6db7-442a-a262-a9f6c12f85b5  *** 
        
        *** Чек по операции с ID: 7f7aead2-6db7-442a-a262-a9f6c12f85b5 : *** 
        
        {'receipt': {'url': 'http://localhost:3000/documents/receipt_7f7aead2-6db7-442a-a262-a9f6c12f85b5.pdf', 'document': '7f7aead2-6db7-442a-a262-a9f6c12f85b5'}}
      ```
