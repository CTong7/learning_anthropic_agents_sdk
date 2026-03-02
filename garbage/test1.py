from claude_agent_sdk import AssistantMessage, ClaudeSDKClient, ResultMessage, TextBlock, ToolUseBlock, create_sdk_mcp_server, query, ClaudeAgentOptions,tool
import asyncio

'''
to define a custom tool you need to use the SDKClient:
1. define async function with @tool decorator
2. define the mcp server config with useless metadata that is never referenced
3. define agent options 
4. run the client
'''

@tool(name="get-prescription",
    description="""Returns the list of medications that a patient has registed in the medical database. 
    Use this tool whenever a user/patient asks for what medication they have access to.
    Make sure the patient_name you pass in is in all lower case
    """,
    input_schema={"patient_name":str})
async def prescription_tool(args):

    drug_database = {
        "chris":["30mg elvanse","30mg dexamphetamine"],
        "max":["shrooms","modephinal"]
    }

    patient_name = args["patient_name"]

    print(f"---------PRINT STATEMENTS STILL RUN EVEN THOUGH IN SEPERATE SUBPROCESS---")

    try:
        # todo: convert drug_list to a string to return
        drug_list = drug_database[patient_name]
        drug_list_str = " ".join(drug_list)

        
        #tools return a fixed object
        return {
            "content":[
                {
                    "type":"text",
                    "text": drug_list_str
                }
            ]

        }


    except Exception as e:
        # todo: define body returned when tool fails
        return {
            "content":[
                {
                    "type":"text",
                    "text":f"User lookup failed:{e}" #learn: return error message in the text content
                }
            ],
            "is_error":True #learn: this is what you have to add for a failure, add this is_error key

        }

# step 2: create mcp server - none of this metadata is used at all

server = create_sdk_mcp_server(
    name = "tools-server",
    version = "1.0.0",
    tools = [prescription_tool]
)

# step 3: define agent options
options = ClaudeAgentOptions(
    mcp_servers = {"tools-server": server},
    model = "sonnet",
    allowed_tools=["mcp__tools-server__get-prescription"],
    system_prompt = """
    You are a helpful digital pharmacist.

    You run a pharmacy and help registered patients get access to the medication they need.

    Use the relevant mcp tool to handle the user query.
    """

)

async def main():

    async with ClaudeSDKClient(options = options) as client:

        await client.query("Return the prescriptions for jeb bush")

        async for message in client.receive_response():

            if isinstance(message,AssistantMessage):

                for block in message.content:

                    if isinstance(block,ToolUseBlock):
                        print(f"Calling Tool: {block.name} -- input: {block.input}")

            elif isinstance(message,ResultMessage):
                print(f"Pharmacist answer: <{message.result}>")

if __name__=="__main__":
    asyncio.run(main())


