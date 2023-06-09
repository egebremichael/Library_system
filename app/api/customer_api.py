"""
customer_api.py

Routes for the API and logic for managing customers.
"""

from flask import g, request, jsonify, Blueprint

from models.customer import Customer, CustomerDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
customer_api_blueprint = Blueprint("customer_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a customer to the end of the url
#   so we can retrieve a specific customer or the entire list of customers as a JSON object
@customer_api_blueprint.route('/api/v1/customers/', defaults={'customer_id':None}, methods=["GET"])
@customer_api_blueprint.route('/api/v1/customers/<int:customer_id>/', methods=["GET"])
def get_customers(customer_id):
    """
    get_customers can take urls in a variety of forms:
        * /api/v1/customer/ - get all customers
        * /api/v1/customer/1 - get the customer with id 1 (or any other valid id)
        * /api/v1/customer/?search="eggs" - find all customers with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the CustomerDB object with the mysql connection and cursor objects
    customerdb = CustomerDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the customer is not supplied then we are either returning all
    #   customers or any customers that match the search query string.
    if customer_id is None:
        # Logic to find all or multiple customers

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = customerdb.select_all_customers()
        # All customers matching the query string "search"
        else:
            result = customerdb.select_all_customers_by_description(args['search'])
    
    else:
        # Logic to request a specific customer
        # We get a specific customers based on the provided customer ID
        result = customerdb.select_customer_by_id(customer_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the customers found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "customers": result}), 200


@customer_api_blueprint.route('/api/v1/customers/', methods=["POST"])
def add_customer():
    customerdb = SustomerDB(g.mysql_db, g.mysql_cursor)
        
    customer = Customer(request.json['description'])
    result = customerdb.insert_customer(customer)
    
    return jsonify({"status": "success", "id": result['customer_id']}), 200


@customer_api_blueprint.route('/api/v1/customers/<int:customer_id>/', methods=["PUT"])
def update_customer(customer_id):
    customerdb = CustomerDB(g.mysql_db, g.mysql_cursor)

    customer = Customer(request.json['description'])
    customerdb.update_customer(customer_id, customer)
    
    return jsonify({"status": "success", "id": task_id}), 200


@customer_api_blueprint.route('/api/v1/customers/<int:customer_id>/', methods=["DELETE"])
def delete_customer(customer_id):
    customerdb = CustomerDB(g.mysql_db, g.mysql_cursor)

    customerdb.delete_customer_by_id(customer_id)
        
    return jsonify({"status": "success", "id": customer_id}), 200