import requests
import random
import json
from datetime import datetime
from faker import Faker

# URL do servidor Flask
BASE_URL = "http://127.0.0.1:5000"

def generate_fake_data():
    """
    Gera dados fictícios usando Faker.

    Returns:
        dict: Dicionário com dados fictícios de transação.
              - "transactionId" (str): Identificador único para a transação.
              - "productId" (str): Identificador do produto.
              - "productName" (str): Nome do produto.
              - "productCategory" (str): Categoria do produto.
              - "productPrice" (float): Preço do produto.
              - "productQuantity" (int): Quantidade do produto.
              - "prodcutDiscount" (float): Desconto do produto.
              - "productBrand" (str): Marca do produto.
              - "currency" (str): Moeda da transação.
              - "customerId" (str): Identificador do cliente.
              - "transactionDate" (str): Data e hora da transação no formato ISO 8601.
              - "paymentMethod" (str): Método de pagamento usado para a transação.
    """
    fake = Faker()
    user = fake.simple_profile()
    record = {
        "transactionId": fake.uuid4(),
        "productId": random.choice(['prod-001', 'prod-002', 'prod-003', 'prod-004', 'prod-005', 'prod-006', 'prod-007']),
        "productName": random.choice(['notebook', 'celular', 'tablet', 'smartwatch', 'fones de ouvido', 'caixa de som']),
        "productCategory": random.choice(['eletrônicos', 'vestuário', 'alimentação', 'casa e decoração', 'beleza e cuidados pessoais', 'esportes e lazer']),
        "productPrice": round(random.uniform(50, 5000), 2),
        "productQuantity": random.randint(0, 5),
        "productDiscount": round(random.uniform(0, 0.5), 2),
        "productBrand": random.choice(['Apple', 'Samsung', 'Xiaomi', 'Microsoft', 'Sony', 'LG', 'Dell', 'Lenovo', 'Positivo']),
        "currency": random.choice(['BRL', 'USD', 'EUR', 'JPY']),
        "customerId": user['username'],
        "transactionDate": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "paymentMethod": random.choice(['cartão de crédito', 'cartão de débito', 'PIX', 'dinheiro', 'boleto'])
    }
    return record

def generate_transaction_batch(batch_size):
    """
    Gera um lote de dados fictícios de transações.

    Args:
        batch_size (int): Número de transações a serem geradas.

    Returns:
        list: Lista de dicionários representando transações fictícias.
    """
    batch = []
    for _ in range(batch_size):
        transaction = generate_fake_data()
        batch.append(transaction)
    return batch    

def send_json(data):
    """
    Envia dados JSON para o servidor Flask via POST.

    Args:
        data (dict or list): Dados a serem enviados como JSON.

    Returns:
        None
    """
    url = f"{BASE_URL}/upload_transaction"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        print("Dados enviados com sucesso.")
    else:
        print(f"Erro ao enviar dados: {response.json()}")

def get_valid_data():
    """
    Recupera os dados processados e válidos do servidor Flask via GET.

    Returns:
        None
    """
    url = f"{BASE_URL}/get_processed_valid_data"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Dados processados e válidos recebidos:")
        print(response.json())
    else:
        print(f"Erro ao obter dados: {response.json()}")

def get_invalid_data():
    """
    Recupera os dados processados e inválidos do servidor Flask via GET.

    Returns:
        None
    """
    url = f"{BASE_URL}/get_processed_invalid_data"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Dados processados e inválidos recebidos:")
        print(response.json())
    else:
        print(f"Erro ao obter dados: {response.json()}")

if __name__ == "__main__":
    # Gerando dados fictícios
    data = generate_transaction_batch(100)
    
    # Enviando JSON para o servidor Flask
    send_json(data)
    
    # Obtendo dados processados e válidos do servidor Flask
    get_valid_data()

    # Obtendo dados processados e inválidos do servidor Flask
    get_invalid_data()
