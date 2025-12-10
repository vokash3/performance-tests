"""
Pydantic BaseModel-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ
"""
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from tools.fakers import fake


class OperationType(StrEnum):
    """
    Типы операций из API
    """
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    PURCHASE = "PURCHASE"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    """
    Статусы операций из API
    """
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(BaseModel):
    """
    PyDantic модель операции.
    """
    model_config = ConfigDict(populate_by_name=True)
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: str = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    PyDantic модель чека операции.
    """
    url: str
    document: str


class OperationsSummarySchema(BaseModel):
    """
    PyDantic модель статистики по операциям.
    """
    model_config = ConfigDict(populate_by_name=True)
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


class GetOperationsSummaryResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос статистики по операциям.
    """
    model_config = ConfigDict(populate_by_name=True)
    summary: OperationsSummarySchema


class GetOperationsResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос списка операций.
    """
    model_config = ConfigDict(populate_by_name=True)
    operations: list[OperationSchema]


class GetOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос информации об операции.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class GetOperationReceiptResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос чека по операции.
    """
    receipt: OperationReceiptSchema


class GetOperationPathParamsSchema(BaseModel):
    """
    PyDantic модель параметров пути для получения информации об операции.
    """
    operation_id: str


class GetOperationReceiptPathParamsSchema(BaseModel):
    """
    PyDantic модель параметров пути для получения чека по операции.
    """
    operation_id: str


class GetOperationsQuerySchema(BaseModel):
    """
    Параметры запроса для получения списка операций по счёту.
    """
    model_config = ConfigDict(populate_by_name=True)
    account_id: str = Field(alias="accountId")


class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Параметры запроса для получения статистики по операциям по счёту.
    """
    model_config = ConfigDict(populate_by_name=True)
    account_id: str = Field(alias="accountId")


class BaseOperationRequestSchema(BaseModel):
    """
    Базовая структура тела запроса для создания операции.
    """
    model_config = ConfigDict(populate_by_name=True)
    status: OperationStatus
    amount: float
    account_id: str = Field(alias="accountId")
    card_id: str = Field(alias="cardId")


class MakeOperationRequestSchema(BaseModel):
    """
    PyDantic модель тела запроса для создания операции
    с фейковыми данными
    """
    model_config = ConfigDict(populate_by_name=True)
    status: OperationStatus = Field(default_factory=lambda: fake.enum(OperationStatus))
    amount: float = Field(default_factory=lambda: fake.float())
    account_id: str = Field(alias="accountId")  # Необходимо для корректного создания операции
    card_id: str = Field(alias="cardId")  # Необходимо для корректного создания операции


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции комиссии.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeFeeOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции комиссии.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции пополнения.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции пополнения.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции кэшбэка.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции кэшбэка.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции перевода.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeTransferOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции перевода.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции покупки.
    """
    category: str = Field(default_factory=lambda: fake.category())


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции покупки.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции оплаты по счёту.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции оплаты по счёту.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции снятия наличных.
    """
    model_config = ConfigDict(populate_by_name=True)


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции снятия наличных.
    """
    model_config = ConfigDict(populate_by_name=True)
    operation: OperationSchema

# ====== (END) BaseModel-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ (END) ======
