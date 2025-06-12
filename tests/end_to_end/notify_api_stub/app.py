from flask import Flask, request
import dotenv
import json
from jsonschema import validate, ValidationError
import time
import uuid

app = Flask(__name__)

dotenv.load_dotenv()


@app.route('/comms/v1/message-batches', methods=['POST'])
def message_batches():
    json_data = default_response_data() | request.json
    batch_reference = json_data["data"]["attributes"]["messageBatchReference"]
    messages = populate_message_ids(json_data["data"]["attributes"]["messages"])

    if not validate_with_schema(json_data):
        return json.dumps({"error": "Invalid body"}), 422

    return json.dumps({
        "data": {
            "type": "MessageBatch",
            "id": json_data["data"].get("id"),
            "attributes": {
                "messageBatchReference": batch_reference,
                "routingPlan": {
                    "id": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                    "name": "Plan Abc",
                    "version": "ztoe2qRAM8M8vS0bqajhyEBcvXacrGPp",
                    "createdDate": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                },
                "messages": messages
            }
        }
    }), 201


def default_response_data():
    return {
        "data": {
            "id": "2ZljUiS8NjJNs95PqiYOO7gAfJb",
            "attributes": {
                "messageBatchReference": str(uuid.uuid4()),
                "messages": []
            }
        }
    }


def populate_message_ids(messages: list[dict]) -> list[dict]:
    for message in messages:
        message["id"] = uid(27) if not message.get("id") else message["id"]

    return messages


def uid(n) -> str:
    return uuid.uuid4().hex[0:n]


def validate_with_schema(data: dict):
    try:
        schema = json.load(open("schema.json"))
        subschema = schema["paths"]["/v1/message-batches"]["post"]["requestBody"]["content"]["application/vnd.api+json"]["schema"]
        validate(instance=data, schema=subschema)
        return True, ""
    except ValidationError as e:
        return False, e.message
    except KeyError as e:
        return False, f"Invalid body: {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
