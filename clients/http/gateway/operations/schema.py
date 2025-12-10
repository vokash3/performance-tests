"""
Pydantic BaseModel-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ
"""
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


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
    summary: OperationsSummarySchema


class GetOperationsResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос списка операций.
    """
    operations: list[OperationSchema]


class GetOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на запрос информации об операции.
    """
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


class MakeFeeOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции комиссии.
    """


class MakeFeeOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции комиссии.
    """
    operation: OperationSchema


class MakeTopUpOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции пополнения.
    """


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции пополнения.
    """
    operation: OperationSchema


class MakeCashbackOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции кэшбэка.
    """


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции кэшбэка.
    """
    operation: OperationSchema


class MakeTransferOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции перевода.
    """


class MakeTransferOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции перевода.
    """
    operation: OperationSchema


class MakePurchaseOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции покупки.
    """
    category: str


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции покупки.
    """
    operation: OperationSchema


class MakeBillPaymentOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции оплаты по счёту.
    """


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции оплаты по счёту.
    """
    operation: OperationSchema


class MakeCashWithdrawalOperationRequestSchema(BaseOperationRequestSchema):
    """
    PyDantic модель тела запроса для создания операции снятия наличных.
    """


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    PyDantic модель ответа на создание операции снятия наличных.
    """
    operation: OperationSchema

# ====== (END) BaseModel-СТРУКТУРЫ ЗАПРОСОВ И ПАРАМЕТРОВ (END) ======
