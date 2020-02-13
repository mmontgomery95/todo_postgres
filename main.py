import helper
from flask import Flask, request, Response
import json

print(f"Starting {__name__}")
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/item/new", methods=["POST"])
def add_item():
    # get item from the POST body
    req_data = request.get_json()
    item = req_data["item"]

    # add item to the list
    res_data = helper.add_to_list(item)

    # return error if item not added
    if res_data is None:
        response = Response(
            "{'error': 'Item not added - " + item + "'}",
            status=500,
            mimetype="application/json",
        )
        return response

        # return response
    response = Response(json.dumps(res_data), mimetype="application/json")

    return response


@app.route("/items/all")  # method defaults to GET
def get_all_items():
    # get items from helper
    res_data = helper.get_all_items()

    # return response
    response = Response(json.dumps(res_data), mimetype="application/json")
    return response


@app.route("/item/status", methods=["GET"])
def get_item():
    # Get parameter from the URL
    item_name = request.args.get("name")

    # Get items from the helper
    status = helper.get_item(item_name)

    # Return 404 if item not found
    if status is None:
        response = Response(
            "{'error': 'Item Not Found - %s'}" % item_name,
            status=404,
            mimetype="application/json",
        )
        return response

    # Return status
    print("why")
    res_data = {"status": status}

    response = Response(json.dumps(res_data), status=200, mimetype="application/json")
    return response


@app.route("/item/update", methods=["PUT"])
def update_status():
    # get the item from POST body
    req_data = request.get_json()
    item = req_data["item"]
    status = req_data["status"]

    # update item in list
    res_data = helper.update_status(item, status)

    # return error if unable to update status
    if res_data is None:
        response = Response(
            "{'error': 'Error updating item - '" + item + ", " + status + "}",
            status=400,
            mimetype="application/json",
        )
        return response

    response = Response(json.dumps(res_data), mimetype="application/json")

    return response


@app.route("/item/remove", methods=["DELETE"])
def delete_item():
    # get item from POST body
    req_data = request.get_json()
    item = req_data["item"]

    # delete item from list
    res_data = helper.delete_item(item)

    # return error if unable to delete item
    if res_data is None:
        response = Response(
            "{'error': 'Error deleting item - '" + item + "}",
            status=400,
            mimetype="application/json",
        )
        return response

    # return response
    response = Response(json.dumps(res_data), mimetype="application/json")

    return response


if __name__ == "__main__":
    app.run()
