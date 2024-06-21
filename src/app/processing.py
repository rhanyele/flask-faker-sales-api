import logging
import json
import pandas as pd
from model.model import validate_transaction
from database.redis_client import create_client_valid, create_client_invalid, truncate_redis, insert_data

def process_data(transaction_data):
    """
    Processa os dados de transações, validando cada transação e 
    separando-as em transações válidas e inválidas.

    Args:
        transaction_data (pd.DataFrame): DataFrame contendo os dados das transações.
    """
    client_valid = create_client_valid()
    client_invalid = create_client_invalid()

    truncate_redis(client_valid)
    truncate_redis(client_invalid)

    for _, row in transaction_data.iterrows():
        transaction = row.to_dict()
        is_valid, errors = validate_transaction(transaction)
        if is_valid:
            transaction['totalAmount'] = calculate_total_amount(transaction['productQuantity'], transaction['productPrice'])
            transaction['discountAmount'] = calculate_discount(transaction['totalAmount'], transaction['productDiscount'])
            transaction['finalAmount'] = calculate_final_amount(transaction['totalAmount'], transaction['discountAmount'])
            logging.info(f"Dados válidos e processados: {transaction}")
            # Insere a transação válidas e processadas no Redis
            insert_data(client_valid, pd.DataFrame([transaction]))
        else:
            logging.warning(f"Dados inválidos: {transaction}")
            logging.error(f"Erro na criação da transação: {errors}")
            # Formata o erro recebido do Pydantic para um formato chave/valor
            for i, error in enumerate(errors, start=1):
                transaction[f'error {i}'] = f"{error.get('type')} occurred in the {error.get('loc')[0]} field. {error.get('msg')} but got {error.get('input')}."
            # Insere a transação inválida no Redis
            insert_data(client_invalid, pd.DataFrame([transaction]))

def calculate_total_amount(quantity, price):
    """
    Calcula o valor total da transação com base na quantidade e no preço do produto.

    Args:
        quantity (int): Quantidade do produto.
        price (float): Preço unitário do produto.

    Returns:
        float: Valor total da transação.
    """
    total_amount = quantity * price
    return round(total_amount, 2)

def calculate_discount(total, discount):
    """
    Calcula o valor de desconto da transação com base no valor total e na porcentagem de desconto.

    Args:
        total (float): Valor total da transação.
        discount (float): Porcentagem de desconto.

    Returns:
        float: Valor de desconto da transação.
    """
    discount_amount = total * discount
    return round(discount_amount, 2)

def calculate_final_amount(total_amount, discount_amount):
    """
    Calcula o valor final da transação com base no valor total e o valor de desconto.

    Args:
        total_amount (float): Valor total da transação.
        discount_amount (float): Valor de desconto da transação.

    Returns:
        float: Valor final da transação.
    """
    final_amount = total_amount - discount_amount
    return round(final_amount, 2)
