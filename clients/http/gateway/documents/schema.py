from pydantic import BaseModel

"""
PyDantic Schemas for API Documents
"""


class DocumentSchema(BaseModel):
    """
    Schema for document
    """
    url: str
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """
    Schema for tariff document response
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Schema for contract document response
    """
    contract: DocumentSchema
