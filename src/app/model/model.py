from pydantic import BaseModel, ValidationError, Field
from typing import Literal
from uuid import UUID
from datetime import datetime


# Definição do modelo
class TransactionModel(BaseModel):
    """
    Modelo para validação de dados de transações.
    """
    transactionId: UUID
    productId: str
    productName: str
    productCategory: str
    productPrice: float = Field(..., gt=50, le=5000)
    productQuantity: int = Field(..., gt=1, le=5)
    productDiscount: float = Field(..., gt=0, le=0.3)
    productBrand: Literal['Apple', 'Samsung', 'Xiaomi', 'Microsoft', 'Sony', 'LG', 'Dell', 'Lenovo']
    currency: Literal['BRL', 'USD', 'EUR']
    customerId: str
    transactionDate: datetime
    paymentMethod: Literal['cartão de crédito', 'cartão de débito', 'PIX', 'dinheiro']


def validate(data, model):
    """
    Valida os dados criando uma instância do modelo com os dados.

    Args:
        data (dict): Os dados a serem validados.
        model (BaseModel): O modelo usado para validar os dados.

    Returns:
        tuple: (bool, list) True se os dados forem válidos, False e lista de erros caso contrário.
    """
    try:
        # Cria uma instância do modelo
        model(**data)
        return True, None
    except ValidationError as e:
        return False, e.errors()


def validate_transaction(data):
    """
    Valida os dados fornecidos com base no modelo TransactionModel.

    Args:
        data (dict): Os dados a serem validados.

    Returns:
        tuple: (bool, list) True se os dados forem válidos, False e lista de erros caso contrário.
    """
    return validate(data, TransactionModel)
