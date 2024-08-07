from flask import Flask, request, jsonify
from flasgger import Swagger
import logging
from model.model import validate_transaction
from processing import process_data
from database.redis_client import create_client_valid, create_client_invalid, get_all_data

logging.basicConfig(level=logging.INFO, filename="logs/app.log", filemode='w', format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

app = Flask(__name__)
swagger = Swagger(app)

client_valid = create_client_valid()
client_invalid = create_client_invalid()

@app.route('/upload_transaction', methods=['POST'])
def upload_json():
    """
    Endpoint para receber dados de transações via requisição POST.
    ---
    tags:
      - POST
    parameters:
      - in: body
        name: body
        description: JSON contendo os dados da transação
        required: true
        schema:
          type: array
          items:
            type: object
            properties:
              transactionId:
                type: string
              productId:
                type: string
              productName:
                type: string
              productCategory:
                type: string
              productPrice:
                type: number
                format: float
              productQuantity:
                type: integer
              productDiscount:
                type: number
                format: float
              productBrand:
                type: string
              currency:
                type: string
              customerId:
                type: string
              transactionDate:
                type: string
                format: date-time
              paymentMethod:
                type: string
    responses:
      200:
        description: Dados recebidos com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Dados recebidos com sucesso.
      400:
        description: Erro na requisição.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nenhum dado recebido.
    """
    try:
        json_data = request.json
        if json_data:
            logging.info(f"Requisição recebida: {json_data}")
            for transaction in json_data:
                logging.info("Validando contrato da transação: %s", transaction)
                is_valid, errors = validate_transaction(transaction)
                if is_valid:
                    logging.info("Transação válida: %s", transaction)
                    process_data(json_data)
                    return jsonify({"message": "Dados recebidos com sucesso."}), 200
                else:
                    return jsonify({"error": errors}), 400
        else:
            return jsonify({"error": "Nenhum dado recebido."}), 400
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 400

@app.route('/get_processed_valid_data', methods=['GET'])
def get_processed_valid_data():
    """
    Endpoint para obter dados de transações válidas processadas.
    ---
    tags:
      - GET
    responses:
      200:
        description: Dados das transações válidas.
        schema:
          type: array
          items:
            type: object
        examples:
          application/json: [
          "transaction: uuid":  
              {
                "productId": string,
                "productName": string,
                "productCategory": string,
                "productPrice": number,
                "productQuantity": integer,
                "productDiscount": number,
                "productBrand": string,
                "currency": string,
                "customerId": string,
                "transactionDate": date-time,
                "paymentMethod": string
              }
          ]
      404:
        description: Nenhum dado processado encontrado.
        schema:
          type: object
          properties:
            info:
              type: string
              example: Nenhum dado processado encontrado.
      500:
        description: Erro ao obter dados processados.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro ao obter dados processados.
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
    ---
    tags:
      - GET
    responses:
      200:
        description: Dados das transações inválidas, que não estão de acordo com as regras de negócio.
        schema:
          type: array
          items:
            type: object
        examples:
          application/json: [
          "transaction: uuid":
              {
                "productId": string,
                "productName": string,
                "productCategory": string,
                "productPrice": number,
                "productQuantity": integer,
                "productDiscount": number,
                "productBrand": string,
                "currency": string,
                "customerId": string,
                "transactionDate": date-time,
                "paymentMethod": string,
                "error 1": string
              }
          ]
      404:
        description: Nenhum dado processado encontrado.
        schema:
          type: object
          properties:
            info:
              type: string
              example: Nenhum dado processado encontrado.
      500:
        description: Erro ao obter dados processados.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro ao obter dados processados.
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
def helth_check():
    """
    Endpoint raiz para verificar se o servidor está funcionando.
    ---
    tags:
      - GET
    responses:
      200:
        description: Mensagem de boas-vindas.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hello, World!
    """
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)