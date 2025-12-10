# Добавили описание структуры карты
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict


class CardType(StrEnum):
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(StrEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class CardSchema(BaseModel):
    """
    Описание структуры карты.
    """
    model_config = ConfigDict(populate_by_name=True)
    id: str
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: str = Field(alias='accountId')
    card_number: str = Field(alias='cardNumber')
    card_holder: str = Field(alias='cardHolder')
    expiry_date: str = Field(alias='expiryDate')
    payment_system: CardPaymentSystem = Field(alias='paymentSystem')


class CardsPayloadSchema(BaseModel):
    """
    FIXME: к удалению (дублирует IssueVirtualCardRequestSchema) из пункта 7.5
    Структура данных (Pydantic) для создания новой кредитной карты пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


class IssueVirtualCardRequestSchema(BaseModel):
    """
    Структура данных (Pydantic) для выпуска виртуальной карты.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


# Добавили описание структуры ответа выпуска виртуальной карты
class IssueVirtualCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска виртуальной карты.
    """
    card: CardSchema


class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Структура данных (Pydantic) для выпуска физической карты.
    """
    model_config = ConfigDict(populate_by_name=True)
    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


# Добавили описание структуры ответа выпуска физической карты
class IssuePhysicalCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска физической карты.
    """
    card: CardSchema
