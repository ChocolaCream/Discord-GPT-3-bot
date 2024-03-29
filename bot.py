import discord
import openai
import asyncio

openai.api_key = "your-OpenAI-key"

activity = discord.Activity(name='Cat videos', type=discord.ActivityType.watching) # if display game needed replace with: discord.Client(activity=discord.Game(name='Cat games'))

client = discord.Client(intents=discord.Intents.all(), messages=True, activity=activity)

@client.event
async def on_message(message):

    if message.content.startswith("$"):
        #store userID who called command in user
        user = message.author.name
        print("Sender name is: " + user)

        #read memory file
        filename = user + '.txt'
        
        #open memory file for specific user
        try: # check if file already exists or not
            f = open(filename, "r")
        except FileNotFoundError: # file did not pre-exist, create memory file
            print("file does not exist, creating file")
            f = open(filename, "w+")
        else: # file existed
            print("file exists, continuing with program")
        finally: # close file and end
            print("closing file")
            f.close()
        
        #read memory to memory variable
        f = open(filename, "r")
        memory = f.read()
        f.close()

        memoryLength = len(memory)
        print("Length of memory string: " + memoryLength)
        
        if memoryLength > 8000:
            print("Token count estimated above 2000. Shortening string for optimized generation")
            print("Memory length prior to shortening: " + memoryLength)
            memory = memory[memoryLength-8000:]
            memoryLength = len(memory)
            print("Memory length post shortening: " + memoryLength)
        
        #variable msg = message string
        msg = message.content[1:]

        print("bot recived message")
        print("user message is: " + msg)
        print("waiting for openAI API response")

        memory += user + ": " + msg+"""\nFelix: """ #tell GPT-3 to respond to the user message in the API prompt
        model = "text-davinci-003" #replace with "text-ada-001" for simple text
        
        async with message.channel.typing():
            
            responsePassed = openai.Completion.create(
                        model=model, #which GPT-3 model 
                        prompt=memory, #prompt to send API
                        temperature=1.0, #temperature is randomness (higher more random, range 1-0)
                        max_tokens=150, #max length for processing and text generation
                        top_p=0.3,
                        frequency_penalty=0.5,
                        presence_penalty=0.0
                    )
            #get string for response 
            responsePassed = responsePassed.choices[0].text
            print("OpenAI API response recived as: "+ responsePassed)

            # write responce to update file
            memory += responsePassed
            f = open(filename, "w")
            f.write(memory)
            f.close()

            print("Responding with response...")
            #show bot is typing for time (string length*0.01 seconds)
            await asyncio.sleep(len(responsePassed)*0.01)
            #after waiting send response in channel/DM where command was called from
            await message.channel.send(responsePassed)
            
#run the bot 
client.run("your-discord-bot-token")
