from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage,ResultMessage, TextBlock,UserMessage


import asyncio
'''
One of the main benefits of using ClaudeSDK Client is that within the context manager you can add messages to the same conversion id

# learn: we can do this simply by doing multiple client.query() in series
'''

options = ClaudeAgentOptions(
    tools = ["WebSearch"]

)

async def main():

    async with ClaudeSDKClient(options = options) as client:

        #learn: Question 1 in series
        await client.query("Tell me about how claude code works under the hood. This is not officially covered in the documentation")
        print("User question: Tell me about how claude code works under the hood. This is not officially covered in the documentation",end = "\n")

        async for message in client.receive_response():

            if isinstance(message,AssistantMessage):
                # returns list of blocks
                for block in message.content:
                    if isinstance(block,TextBlock):
                        print(f"Answer: {block.text}",end ="\n")



            if isinstance(message,ResultMessage):
                print(f"Answer: {message.result}",end ="\n")

        # #learn: Question 2 in series, using same conversation id
        # await client.query("why is the harness for claude code closed source?")
        # print("User question: why is the harness for claude code closed source? ", end="\n")

        # async for message in client.receive_response():

        #     if isinstance(message,AssistantMessage):
        #         # returns list of blocks
        #         for block in message.content:
        #             if isinstance(block,TextBlock):
        #                 print(f"Answer: {block.text}",end ="\n")



        #     if isinstance(message,ResultMessage):
        #         print(f"Answer: {message.result}",end ="\n")

        # await client.query("what was the first message i asked you verbatim?")
        # print("User question: what was the first message i asked you verbatim?", end="\n")

        # async for message in client.receive_response():

        #     if isinstance(message,AssistantMessage):
        #         # returns list of blocks
        #         for block in message.content:
        #             if isinstance(block,TextBlock):
        #                 print(f"Answer: {block.text}",end ="\n")



        #     if isinstance(message,ResultMessage):
        #         print(f"Answer: {message.result}",end ="\n")


if __name__=="__main__":
    asyncio.run(main())