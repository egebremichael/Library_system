"""
transaction_api.py

Routes for the API and logic for managing transaction.
"""

from flask import g, request, jsonify, Blueprint

from models.transaction import Transaction, TransactionDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
transaction_api_blueprint = Blueprint("transaction_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a transaction to the end of the url
#   so we can retrieve a specific transaction or the entire list of transactions as a JSON object
@transaction_api_blueprint.route('/api/v1/transactions/', defaults={'transaction_id':None}, methods=["GET"])
@transaction_api_blueprint.route('/api/v1/transactions/<int:transaction_id>/', methods=["GET"])
def get_transactions(transaction_id):
    """
    get_transactions can take urls in a variety of forms:
        * /api/v1/transaction/ - get all transactions
        * /api/v1/transaction/1 - get the transaction with id 1 (or any other valid id)
        * /api/v1/transaction/?search="eggs" - find all transactions with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TransactionDB object with the mysql connection and cursor objects
    transactiondb = TransactionDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the transaction is not supplied then we are either returning all
    #   transactions or any transactions that match the search query string.
    if transaction_id is None:
        # Logic to find all or multiple transactions

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = transactiondb.select_all_transactions()
        # All transactions matching the query string "search"
        else:
            result = transactiondb.select_all_transactions_by_description(args['search'])
    
    else:
        # Logic to request a specific transaction
        # We get a specific transactions based on the provided transaction ID
        result = transactiondb.select_transaction_by_id(transaction_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the transactions found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "transactions": result}), 200


@transaction_api_blueprint.route('/api/v1/transactions/', methods=["POST"])
def add_transaction():
    transactiondb = TransactionDB(g.mysql_db, g.mysql_cursor)
        
    transaction = Transaction(request.json['description'])
    result = transactiondb.insert_transaction(transaction)
    
    return jsonify({"status": "success", "id": result['transaction_id']}), 200


@transaction_api_blueprint.route('/api/v1/transactions/<int:transaction_id>/', methods=["PUT"])
def update_transaction(transaction_id):
    transactiondb = TransactionDB(g.mysql_db, g.mysql_cursor)

    transaction = Transaction(request.json['description'])
    transactiondb.update_transaction(transaction_id, transaction)
    
    return jsonify({"status": "success", "id": transaction_id}), 200


@transaction_api_blueprint.route('/api/v1/transactions/<int:transaction_id>/', methods=["DELETE"])
def delete_transaction(transaction_id):
    transactiondb = TransactionDB(g.mysql_db, g.mysql_cursor)

    transactiondb.delete_transaction_by_id(transaction_id)
        
    return jsonify({"status": "success", "id": transaction_id}), 200