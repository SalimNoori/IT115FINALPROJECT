import discord
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the intents the bot will use hello
intents = discord.Intents.default()
intents.message_content = True  # Enable the intent to read message content

# Create an instance of a client with the specified intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Event that runs when the bot is ready"""
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    """Event that runs when a message is received"""
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    # Log the message in the console
    print(f'Message "{user_message}" by {username} on {channel}')

    # Ignore messages sent by the bot itself
    if message.author == client.user: 
        return

    # Check if the message is in the 'random' channel
    if channel == "random":
        if user_message.lower() in ["hello", "hi"]:
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called Ilene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))
        elif user_message.lower() == "ec2 metadata":
            metadata = f"""
            Instance ID: {ec2_metadata.instance_id}
            Instance Type: {ec2_metadata.instance_type}
            Availability Zone: {ec2_metadata.availability_zone}
            Public IPv4: {ec2_metadata.public_ipv4}
            """
            await message.channel.send(f'EC2 Metadata:\n{metadata}')

# Retrieve the bot token from the environment variables
token = os.getenv('TOKEN')

# Run the client with the specified token
client.run(token)
