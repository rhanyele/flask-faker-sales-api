import logging
import pandas as pd
from model.model import validate_transaction

# DataFrames para armazenar transações válidas e inválidas
valid_transactions = pd.DataFrame()
invalid_transactions = pd.DataFrame()


def process_data(transaction_data):
    """
    Processa os dados de transações, validando cada transação e 
    separando-as em transações válidas e inválidas.

    Args:
        transaction_data (pd.DataFrame): DataFrame contendo os dados das transações.
    """
    global valid_transactions
    global invalid_transactions

    valid_list = []
    invalid_list = []

    for _, row in transaction_data.iterrows():
        transaction = row.to_dict()
        is_valid, errors = validate_transaction(transaction)
        if is_valid:
            transaction['totalAmount'] = calculate_total_amount(transaction['productQuantity'],transaction['productPrice'])
            transaction['discountAmount'] = calculate_discount(transaction['totalAmount'],transaction['productDiscount'])
            transaction['finalAmount'] = calculate_final_amount(transaction['totalAmount'],transaction['discountAmount'])
            logging.info(f"Dados processados: {transaction}")
            valid_list.append(transaction)
        else:
            logging.warning(f"Dados inválidos: {transaction}")
            logging.error(f"Erro na criação da transação: {errors}")
            transaction['errors'] = errors
            invalid_list.append(transaction)

    if valid_list:
        valid_transactions = pd.DataFrame(valid_list)
    if invalid_list:
        invalid_transactions = pd.DataFrame(invalid_list)


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


def get_valid_transactions():
    """
    Retorna as transações válidas processadas.

    Returns:
        pd.DataFrame: DataFrame contendo as transações válidas.
    """
    global valid_transactions
    return valid_transactions


def get_invalid_transactions():
    """
    Retorna as transações inválidas processadas.

    Returns:
        pd.DataFrame: DataFrame contendo as transações inválidas.
    """
    global invalid_transactions
    return invalid_transactions
