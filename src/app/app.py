from flask import Flask, request, jsonify
import pandas as pd
import logging
from processing import process_data
from database.redis_client import create_client_valid, create_client_invalid, get_all_data

logging.basicConfig(level=logging.INFO, filename="logs/app.log", filemode='w', format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

app = Flask(__name__)

client_valid = create_client_valid()
client_invalid = create_client_invalid()

@app.route('/upload_transaction', methods=['POST'])
def upload_json():
    """
    Endpoint para receber dados de transações via requisição POST.

    Returns:
        Response: JSON com mensagem de sucesso ou erro.
    """
    try:
        json_data = request.json
        if json_data:
            logging.info(f"Requisição recebida: {json_data}")
            df = pd.DataFrame(json_data)
            process_data(df)
            return jsonify({"message": "Dados recebidos com sucesso."}), 200
        else:
            return jsonify({"error": "Nenhum dado recebido."}), 400
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 400

@app.route('/get_processed_valid_data', methods=['GET'])
def get_processed_valid_data():
    """
    Endpoint para obter dados de transações válidas processadas.

    Returns:
        Response: JSON contendo os dados das transações válidas.
    """ 
    try:
        data_redis = get_all_data(client_valid)
        if not data_redis:
            return jsonify({"info": "Nenhum dado processado encontrado."}), 404
        return jsonify(data_redis), 200
    except Exception as e:
        logging.error(f"Erro ao obter dados processados: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/get_processed_invalid_data', methods=['GET'])
def get_processed_invalid_data():
    """
    Endpoint para obter dados de transações inválidas processadas.

    Returns:
        Response: JSON contendo os dados das transações inválidas e mensagem de erro.
    """
    try:
        data_redis = get_all_data(client_invalid)
        if not data_redis:
            return jsonify({"info": "Nenhum dado processado encontrado."}), 404
        return jsonify(data_redis), 200
    except Exception as e:
        logging.error(f"Erro ao obter dados processados: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """
    Endpoint raiz para verificar se o servidor está funcionando.

    Returns:
        Response: JSON com uma mensagem de boas-vindas.
    """
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)