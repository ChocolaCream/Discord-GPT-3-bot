import discord
import openai
import asyncio

openai.api_key = "your-OpenAI-key"

activity = discord.Activity(name='Cat videos', type=discord.ActivityType.watching) # if display game needed replace with: discord.Client(activity=discord.Game(name='Cat games'))

client = discord.Client(intents=discord.Intents.all(), messages=True, activity=activity)

@client.event
async def on_message(message):
    #initialize string to be used for openAI API prompt 
    promptText = """Respond to messages:"""

    if message.author == client.user:
        emoji = '❤'
        await message.add_reaction(emoji)
        return
    if message.content.startswith("$"):
        #store userID who called command in user
        user = message.author
        
        #variable msg = message string
        msg = message.content[1:]

        print("bot recived message")
        print("user message is: " + msg)
        print("waiting for openAI API response")

        promptText += msg+"""\nRespond here: """ #tell GPT-3 to respond to the user message in the API prompt
        model = "text-davinci-002" #replace with "text-ada-001" for simple text
        async with message.channel.typing():
            responsePassed = openai.Completion.create(
                        model=model, #which GPT-3 model 
                        prompt=promptText, #prompt to send API
                        temperature=1.0, #temperature is randomness (higher more random, range 1-0)
                        max_tokens=150, #max length for processing and text generation
                        top_p=0.3,
                        frequency_penalty=0.5,
                        presence_penalty=0.0
                    )
            #get string for response 
            responsePassed = responsePassed.choices[0].text
            print("OpenAI API response recived as: "+ responsePassed)
            print("Responding with response...")
            #show bot is typing for time (string length*0.1 seconds)
            await asyncio.sleep(len(responsePassed)*0.1)
            #after waiting send response in channel/DM where command was called from
            await message.channel.send(responsePassed)
            
#run the bot 
client.run("your-discord-bot-token")
