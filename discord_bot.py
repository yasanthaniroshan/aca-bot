import os, discord, asyncio
from replit import db
from all_massages import *

api_key = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())


async def send_private_msg(message, user):
  await user.send(message)


async def register_student(message):
  try:
    registration_number, student_name = message.author.nick.replace(
      " ", "").split("-")
  except ValueError:
    await message.channel.send(INCORRECT_NICKNAME, reference=message)
    return False

  if registration_number.isnumeric() and len(
      registration_number) == 5 and message.content == registration_number:
      if registration_number not in db["RegisteredStudents"]:
        databaserecord = db["RegisteredStudents"]
        databaserecord[registration_number] = {
          "Name": student_name,
          "UserId": message.author.id
        }
        db["RegisteredStudents"] = databaserecord
      
  
        asyncio.create_task(send_private_msg(REGISTRED, message.author))
      role = await discord.utils.get("1073828209428279316")
      message.author.add_roles(role)
      return True
  
  else:
    await message.channel.send(INCORRECT_REGISTRATION_NUMBER,
                               reference=message)
    return False


async def channels_list():
  for guild in client.guilds:
    for channel in guild.channels:
      print(channel, channel.id)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  channels_list


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.channel.name == 'registration':
    new_registration = asyncio.create_task(register_student(message))


client.run(api_key)
