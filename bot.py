# Import necessary libraries
import discord  # The Discord library to interact with the Discord API
import os  # The OS library to interact with the operating system's environment variables
import random  # The Random library to generate random choices
from ec2_metadata import ec2_metadata  # Import EC2 metadata to access instance-specific information
from dotenv import load_dotenv  # Import the dotenv library to load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Define the intents the bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable the intent to read message content

# Create an instance of a client with the specified intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Event that runs when the bot is ready to be used."""
    print(f"Logged in as {client.user}")  # Print a message to the console indicating the bot is ready

@client.event
async def on_message(message):
    """Event that runs when a message is received in a channel."""
    # Extract the username from the message author (format: username#discriminator)
    username = str(message.author).split("#")[0]
    # Extract the channel name where the message was sent
    channel = str(message.channel.name)
    # Extract the content of the message
    user_message = str(message.content)

    # Log the received message in the console for debugging and monitoring purposes
    print(f'Message "{user_message}" by {username} on {channel}')

    # Ignore any messages sent by the bot itself to prevent it from responding to its own messages
    if message.author == client.user: 
        return

    # Check if the message is in the 'random' channel
    if channel == "random":
        # Respond to greeting messages with a personalized greeting
        if user_message.lower() in ["hello", "hi"]:
            await message.channel.send(f'Hello {username}')
            return
        # Respond to goodbye messages with a personalized farewell
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        # Respond to a request for a joke with a random joke from a predefined list
        elif user_message.lower() == "tell me a joke":
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called Ilene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))
        # Respond to a request for EC2 metadata with information about the current EC2 instance
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
