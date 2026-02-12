import anthropic

client = anthropic.Anthropic()
#learn: every tool is a json object
#! json doesn't support multiline strings since its a data format not a programing language like python, it won't compile your stuff 
# ! you can't add comments inline of a json schema, again its not a programming language it will literally absorb the coment and break the schema
# learn: however, right now we are defining a python object NOT a json schema so comments are fine
# json schemas are always strings
# json.dumps() is fine on a python dict with comments since python ignores comments, it doesn't even store them in ememory, they are removed in parsing stage
# learn: json is always sent on network as '{key1:value1,key2:value2}' in single quotes, gpt will ignore that when showing you the schema but thats what happens
# json iS JUST A DATA FORMAT NOT A LANGUAGE

get_amex_transactions = {
    "name":"get_amex_transactions",
    "description": "Get all credit card transactions from an amex credit card monthly statement", #todo: needs more detail
    "input_schmea":{
        "type":"object", #learn: always
        "properties":{ #todo: stores your input parameters
            "transaction":{
                "type":"object",
                # learn: each parameter is itself a simple json object which has type and description
                "properties":{
                    "transaction_date":{
                        "type":"string",
                        "description":"The date the transaction occured as day/month/year."

                    },

                    ""
                }
            }

        },
        "required":[] #todo: list of variables that must be returned
    }

}

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    betas=["advanced-tool-use-2025-11-20"],
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"], #learn: add enum key when there are distinct values it can take
                        "description": "The unit of temperature"
                    }
                },
                "required": ["location"]
            },
            "input_examples": [
                {
                    "location": "San Francisco, CA",
                    "unit": "fahrenheit"
                },
                {
                    "location": "Tokyo, Japan",
                    "unit": "celsius"
                },
                {
                    "location": "New York, NY"  # 'unit' is optional
                }
            ]
        }
    ],
    messages=[
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]
)