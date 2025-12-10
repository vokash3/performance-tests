from pydantic import BaseModel, ConfigDict, Field

from clients.http.gateway.cards.schema import CardSchema


class AccountSchema(BaseModel):
    """
    Pydantic Model – Описание структуры аккаунта.
    """
    id: str
    type: str
    cards: list[CardSchema]  # Вложенная структура: список карт
    status: str
    balance: float


class GetAccountsQuerySchema(BaseModel):
    """
    Pydantic Model – Структура данных для получения списка счетов пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")


# Добавили описание структуры ответа получения списка счетов
class GetAccountsResponseSchema(BaseModel):
    """
    Pydantic Model – Описание структуры ответа получения списка счетов.
    """
    accounts: list[AccountSchema]


class OpenDepositAccountRequestSchema(BaseModel):
    """
    Pydantic Model – Структура данных для открытия депозитного счета.
    """
    userId: str


# Добавили описание структуры ответа открытия депозитного счета
class OpenDepositAccountResponseSchema(BaseModel):
    """
    Pydantic Model – Описание структуры ответа открытия депозитного счета.
    """
    account: AccountSchema


class OpenSavingsAccountRequestSchema(BaseModel):
    """
    Pydantic Model – Структура данных для открытия сберегательного счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")


# Добавили описание структуры ответа открытия сберегательного счета
class OpenSavingsAccountResponseSchema(BaseModel):
    """
    Pydantic Model – Описание структуры ответа открытия сберегательного счета.
    """
    account: AccountSchema


class OpenDebitCardAccountRequestSchema(BaseModel):
    """
    Pydantic Model – Структура данных для открытия дебетового счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")


# Добавили описание структуры ответа открытия дебетового счета
class OpenDebitCardAccountResponseSchema(BaseModel):
    """
    Pydantic Model – Описание структуры ответа открытия дебетового счета.
    """
    account: AccountSchema


class OpenCreditCardAccountRequestSchema(BaseModel):
    """
    Pydantic Model – Структура данных для открытия кредитного счета.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias="userId")


# Добавили описание структуры ответа открытия кредитного счета
class OpenCreditCardAccountResponseSchema(BaseModel):
    """
    Pydantic Model – Описание структуры ответа открытия кредитного счета.
    """
    account: AccountSchema
