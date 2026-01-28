# QA Performance Engineer

<img src="https://cdn.stepik.net/media/cache/images/courses/242935/cover_cE4uVIf/46ed8cc5a9b8982bd8e91ff34374a376.png" alt="Course cover" height="230" width="230">

Проект для взаимодействия с тестовой банковской системой в
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

### URLs

- HTTP-GATEWAY -> http://155.212.171.137:8003
- GRPC-GATEWAY -> grpc://155.212.171.137:9003

---

### Задания

- [Подготовка к запуску](#подготовка-к-запуску)


- [Task 7.1 – Создание депозитного счёта](#task-71--создание-депозитного-счёта)
- [Task 7.2 – Получение чека по операции](#task-72--получение-чека-по-операции)
- [Task 7.3 – Написание HTTP API клиента (Cards)](#task-73--написание-http-api-клиента-cards)
- [Task 7.4 – Реализация HTTP API клиентов (Operations)](#task-74--реализация-http-api-клиентов-operations)
- [Task 7.5 #1 – Практика использования HTTP API-клиентов: получение документов по счету (Documents)](#task-75-1--практика-использования-http-api-клиентов-получение-документов-по-счету-documents)
- [Task 7.5 #2 – Практика использования HTTP API-клиентов: создание операции пополнения счета (Operations)](#task-75-2--практика-использования-http-api-клиентов-создание-операции-пополнения-счета-operations)
- [Task 8.1 – Практика написания Pydantic-моделей](#81--практика-написания-pydantic-моделей)
- [Task 8.2 #1 – Pydantic в API клиентах: документы](#82-1--pydantic-в-api-клиентах-документы)
- [Task 8.2 #2 – Pydantic в API клиентах: операции](#82-2--pydantic-в-api-клиентах-операции)
- [Task 8.3 – Pydantic в API клиентах: счета](#83--практика-работы-с-генерацией-случайных-данных-faker)
- [Task 9.1 – Практика работы с grpcio](#91--практика-работы-с-grpcio)
- [Task 9.2 – Практикуемся в работе с grpcio: получение чека по операции](#92--практикуемся-в-работе-с-grpcio-получение-чека-по-операции)
- [Task 9.3 – Практика: Написание gRPC API клиента (gRPC – Cards)](#93--практика-написание-grpc-api-клиента-grpc--cards)
- [Task 9.4 – Практика реализации gRPC API клиентов: OperationsGatewayService](#94--практика-реализации-grpc-api-клиентов-operationsgatewayservice)
- [Task 9.5 #1 – Практика использования API-клиентов: получение документов по счету](#95-1--практика-использования-api-клиентов-получение-документов-по-счету)
- [Task 9.5 #2 – Практика использования API-клиентов: создание операции пополнения счета](#95-2--практика-использования-api-клиентов-создание-операции-пополнения-счета)
- [Task 10.1 – Практика: написание нагрузочного сценария открытия дебетового счёта](#101-task--практика-написание-нагрузочного-сценария-открытия-дебетового-счёта)
- [Task 10.3 – Практика: Применение HTTP API клиентов в нагрузочном сценарии (UsersGatewayHTTPClient, AccountsGatewayHTTPClient)](#103-task--практика-применение-http-api-клиентов-в-нагрузочном-сценарии-usersgatewayhttpclient-accountsgatewayhttpclient)
- [Task 10.5 – Практика: Применение gRPC API клиентов в нагрузочном тестировании](#105--практика-применение-grpc-api-клиентов-в-нагрузочном-тестировании)
- [Task 10.6 – Практика: Использование TaskSet для HTTP и gRPC API-клиентов](#106--практика-использование-taskset-для-http-и-grpc-api-клиентов)
- [Task 10.7 Работа с настройками Locust](#107-работа-с-настройками-locust)
- [Task 11.2 – Практика: доработка сидинг-билдера](#112--практика-доработка-сидинг-билдера)

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

---

## Task 7.5 #1 – Практика использования HTTP API-клиентов: получение документов по счету (Documents)

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **api_client_get_documents.py**
  ```bash
  python api_client_get_documents.py
  ```

    - ### Пример успешного выполнения:
      ```
        Create user response: {
            "user": {
                "email": "user_1765275266.360575@example.com",
                "firstName": "Сидор",
                "id": "7a6e5202-8d4b-4f6f-9af3-39c33e2557b9",
                "lastName": "Сысоев",
                "middleName": "Витальевич",
                "phoneNumber": "8 979 050 96 80"
            }
        }
        Open credit card account response: {
            "account": {
                "balance": 25000.0,
                "cards": [
                    {
                        "accountId": "7f6f6a4a-5949-4f23-9472-ffd4264b8a3d",
                        "cardHolder": "Сидор Сысоев",
                        "cardNumber": "30565401651043",
                        "cvv": "882",
                        "expiryDate": "2032-12-07",
                        "id": "5f037ee5-9c0f-4585-9e68-4f4180ea2728",
                        "paymentSystem": "MASTERCARD",
                        "pin": "3314",
                        "status": "ACTIVE",
                        "type": "VIRTUAL"
                    },
                    {
                        "accountId": "7f6f6a4a-5949-4f23-9472-ffd4264b8a3d",
                        "cardHolder": "Сидор Сысоев",
                        "cardNumber": "213170423497134",
                        "cvv": "717",
                        "expiryDate": "2032-12-07",
                        "id": "bf634e38-eac5-417a-a76b-a89a4e0307bd",
                        "paymentSystem": "MASTERCARD",
                        "pin": "0887",
                        "status": "ACTIVE",
                        "type": "PHYSICAL"
                    }
                ],
                "id": "7f6f6a4a-5949-4f23-9472-ffd4264b8a3d",
                "status": "ACTIVE",
                "type": "CREDIT_CARD"
            }
        }
        Get tariff document response: {
            "tariff": {
                "document": "Debate look economic mouth notice yet suddenly his.",
                "url": "http://localhost:3000/documents/tariff_7f6f6a4a-5949-4f23-9472-ffd4264b8a3d.pdf"
            }
        }
      ```

---

## Task 7.5 #2 – Практика использования HTTP API-клиентов: создание операции пополнения счета (Operations)

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **api_client_make_top_up_operation.py**
  ```bash
  python api_client_make_top_up_operation.py
  ```

    - ### Пример успешного выполнения:
      ```
        Create user response: {
            "user": {
                "email": "user_1765283214.914686@example.com",
                "firstName": "Олимпий",
                "id": "1c95577c-4283-48cb-91db-ac72438c31ed",
                "lastName": "Копылов",
                "middleName": "Владленович",
                "phoneNumber": "8 407 287 17 84"
            }
        }
        Open debit card account response: {
            "account": {
                "balance": 0.0,
                "cards": [
                    {
                        "accountId": "14d52946-004a-41f3-9e7f-ca44a202f918",
                        "cardHolder": "Олимпий Копылов",
                        "cardNumber": "6011147407731903",
                        "cvv": "242",
                        "expiryDate": "2032-12-07",
                        "id": "0e5cbb61-c98c-43d1-b1cd-c30959617dc7",
                        "paymentSystem": "MASTERCARD",
                        "pin": "7057",
                        "status": "ACTIVE",
                        "type": "VIRTUAL"
                    },
                    {
                        "accountId": "14d52946-004a-41f3-9e7f-ca44a202f918",
                        "cardHolder": "Олимпий Копылов",
                        "cardNumber": "30464668099940",
                        "cvv": "721",
                        "expiryDate": "2032-12-07",
                        "id": "03d40f8d-6685-480b-aa09-083e81c91d05",
                        "paymentSystem": "MASTERCARD",
                        "pin": "1789",
                        "status": "ACTIVE",
                        "type": "PHYSICAL"
                    }
                ],
                "id": "14d52946-004a-41f3-9e7f-ca44a202f918",
                "status": "ACTIVE",
                "type": "DEBIT_CARD"
            }
        }
        Make top up operation response: {
            "operation": {
                "accountId": "14d52946-004a-41f3-9e7f-ca44a202f918",
                "amount": 55.77,
                "cardId": "0e5cbb61-c98c-43d1-b1cd-c30959617dc7",
                "category": "money_in",
                "createdAt": "2025-12-09T12:26:55.484703",
                "id": "dab0b57c-7fbd-419a-aa68-f2201529f11c",
                "status": "COMPLETED",
                "type": "TOP_UP"
            }
        }
      ```

---

## 8.1 – Практика написания Pydantic-моделей

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Для проверки моделей запускаем **pydantic_create_user.py**
  ```bash
  python pydantic_create_user.py
  ```

    - ### Пример успешной валидации:
    ```
    Валидация CreateUserRequestSchema прошла успешно:
    email='user_1765322244.4291048@example.com' first_name='Твердислав' last_name='Гусев' middle_name='Ефимьевич' phone_number='8 697 611 31 75'
    
    CreateUserResponseSchema успешно сформирован:
    {
      "user": {
        "id": "12345",
        "email": "user_1765322244.4291048@example.com",
        "first_name": "Твердислав",
        "last_name": "Гусев",
        "middle_name": "Ефимьевич",
        "phone_number": "8 697 611 31 75"
      }
    }
    ```

## 8.2 #1 – Pydantic в API клиентах: документы

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **api_client_get_documents.py**
  ```bash
  python api_client_get_documents.py
  ```

    - ### Пример успешного выполнения:
      ```
        Create user response: user=UserSchema(id='06a55b4f-c41d-4ccb-9492-fc06b470e757', email='user.1765387643.159325@example.com', last_name='Кулагин', first_name='Фирс', middle_name='Феликсович', phone_number='+7 (450) 933-7452')
        Open credit card account response: {
            "account": {
                "id": "92fb4d32-3715-4ae1-8c3a-252db81f1348",
                "type": "CREDIT_CARD",
                "cards": [
                    {
                        "id": "f7b284c7-8d4a-4da0-baa6-b999217504a6",
                        "pin": "9029",
                        "cvv": "439",
                        "type": "VIRTUAL",
                        "status": "ACTIVE",
                        "account_id": "92fb4d32-3715-4ae1-8c3a-252db81f1348",
                        "card_number": "3556992744659269",
                        "card_holder": "Фирс Кулагин",
                        "expiry_date": "2032-12-08",
                        "payment_system": "MASTERCARD"
                    },
                    {
                        "id": "b098f3c8-eff9-4e54-b957-dd4224e756ad",
                        "pin": "5156",
                        "cvv": "510",
                        "type": "PHYSICAL",
                        "status": "ACTIVE",
                        "account_id": "92fb4d32-3715-4ae1-8c3a-252db81f1348",
                        "card_number": "4977245343353100",
                        "card_holder": "Фирс Кулагин",
                        "expiry_date": "2032-12-08",
                        "payment_system": "MASTERCARD"
                    }
                ],
                "status": "ACTIVE",
                "balance": 25000.0
            }
        }
        Get tariff document response: {
            "tariff": {
                "url": "http://localhost:3000/documents/tariff_92fb4d32-3715-4ae1-8c3a-252db81f1348.pdf",
                "document": "Anything nor security town past daughter field."
            }
        }
      ```

---

## 8.2 #2 – Pydantic в API клиентах: операции

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем **api_client_make_top_up_operation.py**
  ```bash
  python api_client_make_top_up_operation.py
  ```

    - ### Пример успешного выполнения:
      ```
        Create user response: user=UserSchema(id='f47d2d0f-9ab8-4fa1-a96c-c8d35743b7a1', email='user.1765387982.77933@example.com', last_name='Некрасов', first_name='Корнил', middle_name='Богданович', phone_number='8 638 670 7547')
        Open debit card account response: {
            "account": {
                "id": "01e1d9ee-e3eb-4ec5-a86c-7726f62bedf6",
                "type": "DEBIT_CARD",
                "cards": [
                    {
                        "id": "1b432e45-3c7f-4bc5-97e4-b9557c0eefdf",
                        "pin": "4178",
                        "cvv": "945",
                        "type": "VIRTUAL",
                        "status": "ACTIVE",
                        "account_id": "01e1d9ee-e3eb-4ec5-a86c-7726f62bedf6",
                        "card_number": "6011875740421663",
                        "card_holder": "Корнил Некрасов",
                        "expiry_date": "2032-12-08",
                        "payment_system": "MASTERCARD"
                    },
                    {
                        "id": "bc9c94c3-a9c3-4a43-94b7-7dfd6ab31e50",
                        "pin": "1528",
                        "cvv": "060",
                        "type": "PHYSICAL",
                        "status": "ACTIVE",
                        "account_id": "01e1d9ee-e3eb-4ec5-a86c-7726f62bedf6",
                        "card_number": "3529422293132280",
                        "card_holder": "Корнил Некрасов",
                        "expiry_date": "2032-12-08",
                        "payment_system": "MASTERCARD"
                    }
                ],
                "status": "ACTIVE",
                "balance": 0.0
            }
        }
        Make top up operation response: {
            "operation": {
                "id": "fb496907-402a-451f-a473-e2017292a5ab",
                "type": "TOP_UP",
                "status": "COMPLETED",
                "amount": 55.77,
                "card_id": "1b432e45-3c7f-4bc5-97e4-b9557c0eefdf",
                "category": "money_in",
                "created_at": "2025-12-10T17:33:03.722311",
                "account_id": "01e1d9ee-e3eb-4ec5-a86c-7726f62bedf6"
            }
        }
      ```

## 8.3 – Практика работы с генерацией случайных данных (Faker)

<img src="https://i.pinimg.com/736x/f6/f8/26/f6f82627bd1ddad1e00d716917f1960a.jpg" alt="Task" height="50" width="50">

- Запускаем
    - _api_client_get_user.py_
    - _api_client_get_documents.py_
    - _api_client_issue_physical_card.py_
    - _api_client_make_top_up_operation.py_
      ```bash
      python api_client_make_top_up_operation.py
      python api_client_get_documents.py
      python api_client_issue_physical_card.py
      python api_client_make_top_up_operation.py
      ```
      **Должны выполняться без ошибок!**

---

## 9.1 – Практика работы с grpcio

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем
    - **_grpcio_open_debit_card_account.py_**
      ```bash
      python grpcio_open_debit_card_account.py
      ```
        - ### Пример успешного выполнения:
          ```
          Create user response: user {
            id: "553e146c-ee7d-43e0-8e54-19fab082b174"
            email: "1765455072.771892.evse1984@example.net"
            last_name: "Потапов"
            first_name: "Кузьма"
            middle_name: "Спартак"
            phone_number: "8 253 079 17 14"
          }
          
          Get debit card account response: account {
            id: "ff89b4e8-d41e-4ccc-b488-6050879d0d92"
            type: ACCOUNT_TYPE_DEBIT_CARD
            cards {
              id: "6c93e7f5-8833-4982-96af-1a5e2eea49d6"
              pin: "2885"
              cvv: "635"
              type: CARD_TYPE_VIRTUAL
              status: CARD_STATUS_ACTIVE
              account_id: "ff89b4e8-d41e-4ccc-b488-6050879d0d92"
              card_number: "3549469535051634"
              card_holder: "Кузьма Потапов"
              expiry_date: "09-12-2032"
              payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
            }
            cards {
              id: "6529f2d7-cf5d-4955-bd57-04f2de78779f"
              pin: "8402"
              cvv: "918"
              type: CARD_TYPE_PHYSICAL
              status: CARD_STATUS_ACTIVE
              account_id: "ff89b4e8-d41e-4ccc-b488-6050879d0d92"
              card_number: "4614568630436471"
              card_holder: "Кузьма Потапов"
              expiry_date: "09-12-2032"
              payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
            }
            status: ACCOUNT_STATUS_ACTIVE
          }
          ```

---

## 9.2 – Практикуемся в работе с grpcio: получение чека по операции

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем
    - **_grpcio_get_operation_receipt.py_**
      ```bash
      python grpcio_get_operation_receipt.py
      ```
        - ### Пример успешного выполнения:
          ```
            Create user response: user {
              id: "32089d49-0b77-458e-b490-7e9e12a38dc6"
              email: "1765456826.456606.aleksandra41@example.com"
              last_name: "Елисеев"
              first_name: "Валерьян"
              middle_name: "Конон"
              phone_number: "8 381 582 5414"
            }
            
            Open debit card account response: account {
              id: "54561c25-54b3-4ab1-b9d0-54e738b42bcc"
              type: ACCOUNT_TYPE_DEBIT_CARD
              cards {
                id: "aa0741c6-e589-4106-9c75-61e363943c73"
                pin: "5347"
                cvv: "680"
                type: CARD_TYPE_VIRTUAL
                status: CARD_STATUS_ACTIVE
                account_id: "54561c25-54b3-4ab1-b9d0-54e738b42bcc"
                card_number: "676107779644"
                card_holder: "Валерьян Елисеев"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              cards {
                id: "1d5f133a-2ec7-4051-87b6-c29af9666bb4"
                pin: "6360"
                cvv: "6654"
                type: CARD_TYPE_PHYSICAL
                status: CARD_STATUS_ACTIVE
                account_id: "54561c25-54b3-4ab1-b9d0-54e738b42bcc"
                card_number: "213116182994407"
                card_holder: "Валерьян Елисеев"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              status: ACCOUNT_STATUS_ACTIVE
            }
            
            Make top up operation response: operation {
              id: "8079589a-9654-4b61-89e4-3f5cb34bc00b"
              type: OPERATION_TYPE_TOP_UP
              status: OPERATION_STATUS_COMPLETED
              amount: 563.969970703125
              card_id: "aa0741c6-e589-4106-9c75-61e363943c73"
              category: "money_in"
              created_at: "11-12-2025 12:40:27"
              account_id: "54561c25-54b3-4ab1-b9d0-54e738b42bcc"
            }
            
            Get operation receipt response: receipt {
              url: "http://localhost:3000/documents/receipt_8079589a-9654-4b61-89e4-3f5cb34bc00b.pdf"
              document: "8079589a-9654-4b61-89e4-3f5cb34bc00b"
            }
          ```

---

## 9.3 – Практика: Написание gRPC API клиента (gRPC – Cards)

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем
    - **_clients/grpc/gateway/cards/client.py_**
      ```bash
      PYTHONPATH=`pwd` python clients/grpc/gateway/cards/client.py
      ```
        - ### Пример успешного выполнения:
          ```
            Using user_id=553e146c-ee7d-43e0-8e54-19fab082b174, account_id=ff89b4e8-d41e-4ccc-b488-6050879d0d92
            Issue virtual card response: card {
              id: "8cd8788c-c02d-4285-8eda-152b92e8b8e2"
              pin: "1645"
              cvv: "168"
              type: CARD_TYPE_VIRTUAL
              status: CARD_STATUS_ACTIVE
              account_id: "ff89b4e8-d41e-4ccc-b488-6050879d0d92"
              card_number: "4224465181104024"
              card_holder: "Кузьма Потапов"
              expiry_date: "09-12-2032"
              payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
            }
            
            Issue physical card response: card {
              id: "c59bd2c4-74b2-41ec-9b66-d4ef797506c1"
              pin: "4185"
              cvv: "851"
              type: CARD_TYPE_PHYSICAL
              status: CARD_STATUS_ACTIVE
              account_id: "ff89b4e8-d41e-4ccc-b488-6050879d0d92"
              card_number: "3501797545457433"
              card_holder: "Кузьма Потапов"
              expiry_date: "09-12-2032"
              payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
            }
          ```

---

## 9.4 – Практика реализации gRPC API клиентов: OperationsGatewayService

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем для проверки работы методов
    - **_clients/grpc/gateway/operations/client.py_**
      ```bash
      PYTHONPATH=`pwd` python clients/grpc/gateway/operations/client.py
      ```
        - ### Пример успешной проверки:
          ```
            STATUS для операций:  1
            ==============================================
            Create user response: user {
              id: "248bbdee-6852-4bb8-a900-3a1bd24aaf4d"
              email: "1765461963.1300359.efremovbudimir@example.com"
              last_name: "Калинин"
              first_name: "Доброслав"
              middle_name: "Захар"
              phone_number: "+7 174 854 68 67"
            }
            
            Open debit account response: account {
              id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
              type: ACCOUNT_TYPE_DEBIT_CARD
              cards {
                id: "0348e08c-4433-40ac-b602-79838c697d9e"
                pin: "8158"
                cvv: "173"
                type: CARD_TYPE_VIRTUAL
                status: CARD_STATUS_ACTIVE
                account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
                card_number: "4677627879683906"
                card_holder: "Доброслав Калинин"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              cards {
                id: "826b21f4-25a4-4f19-ad53-cbe09d018e68"
                pin: "9920"
                cvv: "206"
                type: CARD_TYPE_PHYSICAL
                status: CARD_STATUS_ACTIVE
                account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
                card_number: "30051028463757"
                card_holder: "Доброслав Калинин"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              status: ACCOUNT_STATUS_ACTIVE
            }
            
            Using existing card from account: id: "0348e08c-4433-40ac-b602-79838c697d9e"
            pin: "8158"
            cvv: "173"
            type: CARD_TYPE_VIRTUAL
            status: CARD_STATUS_ACTIVE
            account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            card_number: "4677627879683906"
            card_holder: "Доброслав Калинин"
            expiry_date: "09-12-2032"
            payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
            
            Make fee operation response: operation {
              id: "78fa0a55-e9be-43bf-8d56-f8dfde93e095"
              type: OPERATION_TYPE_FEE
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -385.97000122070312
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "fee"
              created_at: "11-12-2025 14:06:03"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make top up operation response: operation {
              id: "e269a2b2-70e3-4166-8c2f-59ae67fcd47a"
              type: OPERATION_TYPE_TOP_UP
              status: OPERATION_STATUS_IN_PROGRESS
              amount: 871.77001953125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "money_in"
              created_at: "11-12-2025 14:06:03"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make cashback operation response: operation {
              id: "9eab5236-24f1-4e4b-8960-e7221b39bfdb"
              type: OPERATION_TYPE_CASHBACK
              status: OPERATION_STATUS_IN_PROGRESS
              amount: 966.20001220703125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "cashback_rewards"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make transfer operation response: operation {
              id: "c7d89ac6-f13f-4d3c-b02e-fc049c7384f1"
              type: OPERATION_TYPE_TRANSFER
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -944.57000732421875
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "transfer"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make purchase operation response: operation {
              id: "bec7fa6f-06a1-4588-8ee1-e8df3662c1b4"
              type: OPERATION_TYPE_PURCHASE
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -585.29998779296875
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "mobile"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make bill payment operation response: operation {
              id: "8364ce6e-36c6-4dbc-89ef-ab6695b3a6fd"
              type: OPERATION_TYPE_BILL_PAYMENT
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -942.4000244140625
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "bill_payment"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Make cash withdrawal operation response: operation {
              id: "73ce8d86-0ade-42e5-9fb8-c07cf576bc84"
              type: OPERATION_TYPE_CASH_WITHDRAWAL
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -778.969970703125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "cash_withdrawal"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Get operations response: operations {
              id: "78fa0a55-e9be-43bf-8d56-f8dfde93e095"
              type: OPERATION_TYPE_FEE
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -385.97000122070312
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "fee"
              created_at: "11-12-2025 14:06:03"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "e269a2b2-70e3-4166-8c2f-59ae67fcd47a"
              type: OPERATION_TYPE_TOP_UP
              status: OPERATION_STATUS_IN_PROGRESS
              amount: 871.77001953125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "money_in"
              created_at: "11-12-2025 14:06:03"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "9eab5236-24f1-4e4b-8960-e7221b39bfdb"
              type: OPERATION_TYPE_CASHBACK
              status: OPERATION_STATUS_IN_PROGRESS
              amount: 966.20001220703125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "cashback_rewards"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "c7d89ac6-f13f-4d3c-b02e-fc049c7384f1"
              type: OPERATION_TYPE_TRANSFER
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -944.57000732421875
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "transfer"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "bec7fa6f-06a1-4588-8ee1-e8df3662c1b4"
              type: OPERATION_TYPE_PURCHASE
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -585.29998779296875
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "mobile"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "8364ce6e-36c6-4dbc-89ef-ab6695b3a6fd"
              type: OPERATION_TYPE_BILL_PAYMENT
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -942.4000244140625
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "bill_payment"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            operations {
              id: "73ce8d86-0ade-42e5-9fb8-c07cf576bc84"
              type: OPERATION_TYPE_CASH_WITHDRAWAL
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -778.969970703125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "cash_withdrawal"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Get operations summary response: summary {
              spent_amount: -3637.21
              received_amount: 871.77
              cashback_amount: 966.2
            }
            
            Get operation response: operation {
              id: "73ce8d86-0ade-42e5-9fb8-c07cf576bc84"
              type: OPERATION_TYPE_CASH_WITHDRAWAL
              status: OPERATION_STATUS_IN_PROGRESS
              amount: -778.969970703125
              card_id: "0348e08c-4433-40ac-b602-79838c697d9e"
              category: "cash_withdrawal"
              created_at: "11-12-2025 14:06:04"
              account_id: "d3d3534f-5d1f-42d5-a7b8-e0f587a6c170"
            }
            
            Get operation receipt response: receipt {
              url: "http://localhost:3000/documents/receipt_73ce8d86-0ade-42e5-9fb8-c07cf576bc84.pdf"
              document: "73ce8d86-0ade-42e5-9fb8-c07cf576bc84"
            }
          ```
            - ‼️ Можем столкнуться с проблемой, если СТАТУС ОТЛИЧЕН ОТ status: **OPERATION_STATUS_IN_PROGRESS** (1) или
              **OPERATION_STATUS_COMPLETED** (2):
              ```
              grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
              status = StatusCode.INTERNAL
              details = "Get receipt: An error occurred (NoSuchKey) when calling the GetObject operation:
              The specified key does not exist."
              debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:13, grpc_message:"Get receipt:
              An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist."}"
              ```

              _Для справки:_
              ```
              DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
              OPERATION_STATUS_UNSPECIFIED: _OperationStatus.ValueType # 0
              OPERATION_STATUS_IN_PROGRESS: _OperationStatus.ValueType # 1
              OPERATION_STATUS_COMPLETED: _OperationStatus.ValueType # 2
              OPERATION_STATUS_FAILED: _OperationStatus.ValueType # 3
              ```

---

## 9.5 #1 – Практика использования API-клиентов: получение документов по счету

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем
    - **_grpc_api_client_get_documents.py_**
      ```bash
      python grpc_api_client_get_documents.py
      ```
        - ### Пример успешного выполнения:
          ```
            Create user response: user {
              id: "a5f260fb-cc18-4688-a7fa-d6495c95b842"
              email: "1765463846.336705.belovandre@example.net"
              last_name: "Кудрявцев"
              first_name: "Исидор"
              middle_name: "Геннадий"
              phone_number: "+7 (078) 978-6409"
            }
            
            Open credit account response: account {
              id: "8ad98b3d-a590-4122-9233-6843004a5675"
              type: ACCOUNT_TYPE_CREDIT_CARD
              cards {
                id: "1bac350a-d7eb-4b8d-b488-19a5b77701ee"
                pin: "4861"
                cvv: "630"
                type: CARD_TYPE_VIRTUAL
                status: CARD_STATUS_ACTIVE
                account_id: "8ad98b3d-a590-4122-9233-6843004a5675"
                card_number: "4974899808594971"
                card_holder: "Исидор Кудрявцев"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              cards {
                id: "08252684-77ed-47e3-a975-23d014496979"
                pin: "6935"
                cvv: "7044"
                type: CARD_TYPE_PHYSICAL
                status: CARD_STATUS_ACTIVE
                account_id: "8ad98b3d-a590-4122-9233-6843004a5675"
                card_number: "2265712697112742"
                card_holder: "Исидор Кудрявцев"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              status: ACCOUNT_STATUS_ACTIVE
              balance: 25000
            }
            
            Tariff document response: tariff {
              url: "http://localhost:3000/documents/tariff_8ad98b3d-a590-4122-9233-6843004a5675.pdf"
              document: "Simply plan everything report."
            }
            
            Get contract document response: contract {
              url: "http://localhost:3000/documents/contract_8ad98b3d-a590-4122-9233-6843004a5675.pdf"
              document: "Bag world nor soldier accept."
            }
          ```

---

## 9.5 #2 – Практика использования API-клиентов: создание операции пополнения счета

<img src="https://media.proglib.io/posts/2021/02/12/f709819f6c3ad08c3771fbc3efecc929.webp" alt="grpc_pic" height="100" width="200">

- Запускаем
    - **_grpc_api_client_make_top_up_operation.py_**
      ```bash
      python grpc_api_client_make_top_up_operation.py
      ```
        - ### Пример успешного выполнения:
          ```
            Create user response: user {
              id: "48bcf67b-041b-41c5-a8a2-80314eebc9fc"
              email: "1765464948.297502.radislav_1996@example.net"
              last_name: "Дроздов"
              first_name: "Ефим"
              middle_name: "Роман"
              phone_number: "+7 645 502 94 79"
            }
            
            Open credit account response: account {
              id: "749013f9-0fed-49c9-92e1-889d06afe986"
              type: ACCOUNT_TYPE_DEBIT_CARD
              cards {
                id: "6b029ee8-55f9-4a14-81a1-3d605e0a1123"
                pin: "0571"
                cvv: "941"
                type: CARD_TYPE_VIRTUAL
                status: CARD_STATUS_ACTIVE
                account_id: "749013f9-0fed-49c9-92e1-889d06afe986"
                card_number: "30279149196523"
                card_holder: "Ефим Дроздов"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              cards {
                id: "9fd926f9-d607-4e48-a902-98ea9096071c"
                pin: "4516"
                cvv: "080"
                type: CARD_TYPE_PHYSICAL
                status: CARD_STATUS_ACTIVE
                account_id: "749013f9-0fed-49c9-92e1-889d06afe986"
                card_number: "5424005450149006"
                card_holder: "Ефим Дроздов"
                expiry_date: "09-12-2032"
                payment_system: CARD_PAYMENT_SYSTEM_MASTERCARD
              }
              status: ACCOUNT_STATUS_ACTIVE
            }
            
            Operation make top up response: operation {
              id: "431445f7-0588-4172-8caf-19d7ce55976f"
              type: OPERATION_TYPE_TOP_UP
              status: OPERATION_STATUS_IN_PROGRESS
              amount: 230.89999389648438
              card_id: "6b029ee8-55f9-4a14-81a1-3d605e0a1123"
              category: "money_in"
              created_at: "11-12-2025 14:55:48"
              account_id: "749013f9-0fed-49c9-92e1-889d06afe986"
            }
          ```

---

# 10.1 Task – Практика: написание нагрузочного сценария открытия дебетового счёта

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

- Запускаем
    ```bash
    python -m locust -f locust_open_debit_card_account.py --class-picker --processes 2 --csv reports/report.csv --csv-full-history --json-file reports/report --html reports/report.html -u 300 -r 10 -t 1m
    ```
- В [WebUI]( http://0.0.0.0:8089) нажимаем button **START**
- Через 1 минуту – тест завершается STOPPED.
- В терминале CTR+C
- Ознакамливаемся с отчётом

**`Уже готовый отчёт лежит в reports/`**

- Краткий вывод по отчёту:
-
    - Основной «узкий» ресурс — именно открытие дебетового счёта: его медиана и хвосты растут почти линейно с ростом
      User Count, при этом ошибок нет, значит, речь о деградации по времени, а не по стабильности.
-
    - После ~150–170 пользователей видно, что RPS уже почти не увеличивается, а задержки продолжают расти — это типичный
      признак того, что система достигла предела пропускной способности и дальше накапливает очередь.

---

# 10.2 Task – Практика: Создание билдеров для HTTP API клиентов Locust (OperationsGatewayHTTPClient, DocumentsGatewayHTTPClient)

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

`Без запуска`

---

# 10.3 Task – Практика: Применение HTTP API клиентов в нагрузочном сценарии (UsersGatewayHTTPClient, AccountsGatewayHTTPClient)

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

- Запускаем
    ```bash
    python -m locust -f locust_open_debit_card_account.py \
  --class-picker \
  --processes 2 \
  --csv reports/locust_api_client_open_debit_card_account_report.csv \
  --csv-full-history --json-file reports/locust_api_client_open_debit_card_account_report \
  --html reports/locust_api_client_open_debit_card_account_report.html \
  -u 300 -r 10 -t 1m
    ```
- В [WebUI]( http://0.0.0.0:8089) нажимаем button **START**
- Через 1 минуту – тест завершается STOPPED.
- В терминале CTR+C
- Ознакамливаемся с отчётом

**`Уже готовый отчёт лежит в reports/locust_api_client_open_debit_card_account_report.html`**

---

# 10.5 – Практика: Применение gRPC API клиентов в нагрузочном тестировании

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

- Запускаем
    ```bash
    python -m locust -f grpc_locust_open_debit_card_account.py --class-picker --processes 4 --html reports/grpc_locust_open_debit_card_account_report.html -u 100 -r 10 -t 3m
    ```

**`Уже готовый отчёт лежит в reports/grpc_locust_open_debit_card_account_report_24122025_2246.html`**

---

# 10.6 – Практика: Использование TaskSet для HTTP и gRPC API-клиентов

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

- Запускаем нагрузку по HTTP:
    ```bash
    python -m locust -f locust_get_accounts.py --headless --processes 4 --html reports/locust_get_accounts.html -u 50 -r 1 -t 1
    ```
- Запускаем нагрузку по gRPC:
    ```bash
    python -m locust -f grpc_locust_get_accounts.py --headless --processes 4 --html reports/grpc_locust_get_accounts.html -u 50 -r 1 -t 1
    ```

**`Уже готовые отчёты лежат в reports: locust_get_accounts.html и grpc_locust_get_accounts.html`**

---

# 10.7 Работа с настройками Locust

<img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Locust-logo.png" alt="locust_logo" height="48" width="200">

- Запускаем нагрузку по HTTP:
    ```bash
    python -m locust --config=./scenarios/http/gateway/get_accounts/v1.0.conf
    ```
- Запускаем нагрузку по gRPC:
    ```bash
    python -m locust --config=./scenarios/grpc/gateway/get_accounts/v1.0.conf
    ```

**
`Готовые отчёты лежат ./scenarios/http/gateway/get_accounts/report.html и ./scenarios/grpc/gateway/get_accounts/report.html`
**

---

# 11.2 – Практика: доработка сидинг-билдера

<img src="https://i.ytimg.com/vi/oh-Dfqa2bjI/maxresdefault.jpg" alt="seed_data" height="100" width="177">

- Запускаем сидинг через gRPC-api:
    ```bash
    python try_seeding.py
    ```

**
`Готовый дамп лежит ./dumps/test_scenario-11-2_seeds.json
**
---