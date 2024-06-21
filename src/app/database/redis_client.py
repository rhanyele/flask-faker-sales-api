import redis

def connect_redis(db):
    """
    Conecta ao servidor Redis especificado.

    Args:
        db (int): Número do banco de dados Redis a ser conectado.

    Returns:
        redis.Redis: Objeto cliente Redis conectado ao banco de dados especificado.
    """
    # redis-db é o nome do container do Redis
    return redis.Redis(host='redis-db', port=6379, db=db)

def truncate_redis(client):
    """
    Limpa (flush) todos os dados do banco de dados Redis.

    Args:
        client (redis.Redis): Cliente Redis conectado ao banco de dados.
    """
    client.flushdb()

def insert_data(client, data):
    """
    Insere os dados do DataFrame no Redis.

    Args:
        client (redis.Redis): Cliente Redis conectado ao banco de dados.
        data: Dados a serem inseridos.
    """
    for row in data.to_dict('records'):
        transaction_id = row['transactionId']
        key = f"transaction:{transaction_id}"
        client.hmset(key, row)

def get_all_data(client):
    """
    Retorna todos os dados armazenados no Redis.

    Args:
        client (redis.Redis): Cliente Redis conectado ao banco de dados.

    Returns:
        dict: Dicionário contendo todos os dados armazenados no Redis.
              A chave é o nome da chave Redis, e o valor é um dicionário representando os campos e valores da chave hash.
    """
    keys = client.keys()
    result = {}
    for key in keys:
        key_str = key.decode('utf-8')
        data = client.hgetall(key)
        data_str = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
        result[key_str] = data_str
    return result

def create_client_valid():
    """
    Cria um cliente conectando-se a o servidor Redis com o número do banco de dados especificado para salvar os dados válidos.

    Returns:
        redis.Redis: Cliente Redis conectado ao banco de dados especificado.
    """
    return connect_redis(0)

def create_client_invalid():
    """
    Cria um cliente conectando-se a o servidor Redis com o número do banco de dados especificado para salvar os dados inválidos.

    Returns:
        redis.Redis: Cliente Redis conectado ao banco de dados especificado.
    """
    return connect_redis(1)