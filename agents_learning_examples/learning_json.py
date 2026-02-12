'''
There are 3 ways to load data in python and send it as json
'''
import json
from pathlib import Path
#learn: Method 1 - define data as a PYTHON DICTIONARY + convert to json 

data = {
    "hi":1
}

# convert python dictionary into json format to send

json_data = json.dumps(data)
print("This is method 1:", end = "\n")
print(json_data)


#learn: Method 2 - define data as a python string in json format+ no need to convert
# this data can be sent directly to the api without conversion because its already a string
json_string = """
{
    "hi":1

}
"""
print("This is method 2:", end = "\n")
print(json_string)

#learn: Method 3 - define data in a .json file + load it into python file + no need to convert
json_path = Path(__file__).resolve().parent / "test.json"

with open(json_path) as file:
    json_string = json.load(file) #! this actually converts it into python dictionary, not a json

print("This is method 3:", end = "\n")

print(type(json_string)) # this is a dictionary