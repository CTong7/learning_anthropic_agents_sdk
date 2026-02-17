
import json
from pydantic import BaseModel, Field
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query


import asyncio

# step 1: define a pydantic class for the output inheriting base model class
class DesiredOutput(BaseModel):
    input_question: str = Field(description="The input question passed to the LLM we are testing")
    ground_truth: str = Field(description="The ground truth answer to the input question")


# step 2: convert the pydantic class to python dictionary .model_json_schema()

json_schema = DesiredOutput.model_json_schema()


# learn: your output_format MUST have 2 keys
'''
1. it must have type key of value : json_schema
2. it must have a schema key = to a json 

'''
# step 3: define the output_format dictionary with the 2 mandatory key names and values
output_format = {
    "type": "json_schema",
    "schema": json_schema
}

options = ClaudeAgentOptions(
    output_format=output_format,
    system_prompt= """
    You are a helpful assistant.

    You will assist me in generating test cases for my legal LLM evaluation.

    Output a single test case for legal contract review and return a valid json.
    """
)

async def main():

    async for message in query(prompt = "generate a eval test case for legal contract review",options = options):

        if isinstance(message,AssistantMessage):

            for block in message.content:
                if isinstance(block,TextBlock):
                    print(f"Answer: {block.text}")

        # learn: result message has a .result key but ALSO a .structured_output value
        # structured_output returns a PYTHON DICTIONARY., which you can slice keys 
        elif isinstance(message,ResultMessage):

            print(message.structured_output,end="\n")
            print(f"this is the final structured ouput type: is it python or string?: {type(message.structured_output)}",end="\n")
            actual_json= json.dumps(message.structured_output)

            print(f"after using json.dumps on the output it becomes a string again not a dict: {type(actual_json)}")



if __name__=="__main__":
    asyncio.run(main())