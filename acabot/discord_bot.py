import os, discord, asyncio, csv
from replit import db
from asgiref.sync import sync_to_async
import pytz
from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.ui import Select, View
from datetime import datetime
from django.conf import settings
import django
from acabot.settings import DATABASES, INSTALLED_APPS

settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
settings.USE_TZ = True
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "false"

django.setup()
from all_masseges import *
from Users.models import User, Students
from attendance.models import Attendance_Student
from Aca_sessions.models import Subjects, Session_details

TIME_ZONE = 'Asia/Kolkata'

VIEWER_ROLE = 1075799892326359170
ADMIN_ROLE = 1075798808623075429
CLASSROOM_ID = 1075794977386414101
TEST_SERVER_ID = 1075802645647872000

runtime_details = None


class runtime():
  in_a_activesession = False
  subject = None
  session_name = None
  classroom = None
  # def __init__(self,activesession,subject,session_name) -> None:
  #    self.in_a_activesession = activesession
  #    self.subject = subject
  #    self.session_name = session_name


api_key = 'MTA3MzU4NDkwNjM5NzA0NDczNg.GVPTEV.2uR1LIj09TPiS8ImJ7D6878qbQv0pXJsNWPu34'

client = commands.Bot(command_prefix="<<<", intents=discord.Intents.all())

async def send_notification(message):
  await client.get_channel(TEST_SERVER_ID).send(message)

@client.command()
async def addrole(user, server_id, role_id):
  server = client.get_guild(server_id)
  role = server.get_role(role_id)
  await discord.Member.add_roles(user, role)
  return True


async def send_private_msg(message, user):
  await user.send(message)


def getting_username(username):
  try:
    index, student_name = username.replace(" ", "").split("-")
    return index
  except:
    return False


# async def register_student(message):
  


# async def channels_list():
#   for guild in client.guilds:
#     for channel in guild.channels:
#       print(channel, channel.id)


async def homework_handler(attachment):
  user = await client.fetch_user(805786909422518293)
  print(user)
  file = await attachment.to_file()
  await user.send(file=file, content="hai")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


def making_embedd_of_Session(subject, Session_name, author_name, avatar):
  embedd = discord.Embed(
    title="Starting New Session",
    description="This Prompt is generated when new session Started",
    color=0x3498DB)
  embedd.set_author(name=f"{author_name}")
  embedd.set_thumbnail(url=f"{avatar}")
  embedd.add_field(name="Subject", value=subject)
  embedd.add_field(name="Session ID", value=Session_name)
  embedd.set_footer(text="This is a Generated View")
  return embedd


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.channel.type is discord.ChannelType.private:
    await message.reply("Bosa Kohomada ithin")
  else:
    if message.channel.name == 'registration':
      new_registration = asyncio.create_task(register_student(message))

    if message.attachments:
      homesended = asyncio.create_task(homework_handler(
        message.attachments[0]))
  await client.process_commands(message)


@client.event
async def on_voice_state_update(member, before, after):
  if member.bot:
    return
  elif runtime_details is not None:
    if runtime_details.in_a_activesession:
      if before.channel == None and after.channel != None:
        try:
          user = User.objects.get(username=getting_username(member.nick))
          student_record = await sync_to_async(Attendance_Student.objects.get)(
            user=user,
            session_name=runtime_details.session_name,
            subject=runtime_details.subject)
          student_record.log_on_at = datetime.now(pytz.timezone(TIME_ZONE))
          student_record.present = True
          student_record.save()
          print("logged-user logged in")
        except Attendance_Student.DoesNotExist:
          student_record = await sync_to_async(
            Attendance_Student.objects.create
          )(user=user,
            session_name=runtime_details.session_name,
            subject=runtime_details.subject,
            present=True,
            log_on_at=datetime.now(pytz.timezone(TIME_ZONE)))
          print("new-user logged In")
      elif before.channel != None and after.channel == None:
        try:
          user = User.objects.get(username=getting_username(member.nick))
          student_record = await sync_to_async(Attendance_Student.objects.get)(
            user=user,
            session_name=runtime_details.session_name,
            subject=runtime_details.subject)
          student_record.log_out_at = datetime.now(pytz.timezone(TIME_ZONE))
          student_record.present = False
          student_record.total_duration = student_record.total_duration + student_record.log_out_at - student_record.log_on_at
          student_record.save()
          print("user left session")
        except Attendance_Student.DoesNotExist:
          print("Error occured")
      elif before.channel != None and after.channel != None:
        try:
          user = User.objects.get(username=getting_username(member.nick))
          student_record = await sync_to_async(Attendance_Student.objects.get)(
            user=user,
            session_name=runtime_details.session_name,
            subject=runtime_details.subject)
          student_record.active_user = True
          student_record.save()
          print(f"{member.nick} left session is active")
        except Attendance_Student.DoesNotExist:
          print("Error occured")
  new_user = str(member.name)
  guild_id = str(member.guild.id)
  if after.channel is None:
    print(member.nick, before.channel.members)
  print(member, after.channel, before.channel)


client.command()


async def endsession(ctx):
  attendance = []
  channel = client.get_channel(CLASSROOM_ID)
  try:
    session_deatils = Session_details.objects.get(
      name=runtime_details.session_name,
      subject=runtime_details.subject,
      started=True,
    )
    for member in channel.members:
      name = getting_username(member.nick)
      if name[0:2] == "22":
        attendance.append(name)
    session_deatils.ended_at = datetime.now(pytz.timezone(TIME_ZONE))
    session_deatils.no_of_students_at_ended = len(attendance)
    session_deatils.ended = True
    session_deatils.total_time = session_deatils.ended_at - session_deatils.started_at
    session_deatils.save()
  except:
    print("Not Started Session")


@client.event
async def on_member_update(before, after):
  if before.nick != after.nick:
    try:
      index, name = after.nick.strip().replace(" ", "").split("-")
      # await send_notification(f"Name - {name} | Index number - {index} has joined server")
      if index[0:2] == "22" and len(index) == 5:
        await addrole(after, after.guild.id, VIEWER_ROLE)
        try:
          user = User.objects.get(username=index)
          student = Students.objects.get(user=user)
        except User.DoesNotExist:
          await send_notification(f"Renamed user - {index} doesn't in database")
        if not student.registered:
          if student.user.username == index:
            student.registered = True
            student.save()
            await send_notification(f"User - {index} | {name} assigned to role {index[0:2]}")
          else:
            await send_notification(f"Renamed user - {index} index and server nicknames are different")
        else:
          await send_notification(f"User - {index} | {name} Already registered")
      elif index == "21" and len(index) == 2:
        await addrole(after, after.guild.id, ADMIN_ROLE)
        await send_notification(f"User - {index} | {name} assigned to role {index[0:2]}")
    except:
      await send_notification(f"{index} | {name} user nickname format is incorrect")


@client.command()
async def start(ctx):
  if ADMIN_ROLE in [role.id for role in ctx.author.guild.roles]:
    global runtime_details
    runtime_details = runtime()
    select = Select(
      placeholder="Select Subject",
      options=option_list_of_subjects,
    )

    async def callback_for_subject_selcet(interaction):
      await interaction.response.send_message("Send me name of session !")

      def checking_reply(message):
        if message.author == interaction.user:
          return message.content

      msg = await client.wait_for('message', check=checking_reply)

      await msg.reply(embed=making_embedd_of_Session(
        Subjects.getting_label((
          select.values[0])), msg.content, msg.author.name, msg.author.avatar))
      runtime_details.in_a_activesession = True
      runtime_details.subject = select.values[0]
      runtime_details.session_name = msg.content
      await connet_to_voice_channel(CLASSROOM_ID)
      await present_marking()

    select.callback = callback_for_subject_selcet
    view = View()
    view.add_item(select)
    await ctx.send("Chooose Subject", view=view)
  else:
    await ctx.reply("You are not allowed to give commands")


async def connet_to_voice_channel(Channel_id):
  channel = client.get_channel(Channel_id)
  await channel.connect()
  print(f"Bot joined to {channel.name}")
  return channel


async def present_marking():
  attendance = []
  channel = client.get_channel(CLASSROOM_ID)
  session_deatils = await sync_to_async(Session_details.objects.create)(
    name=runtime_details.session_name,
    subject=runtime_details.subject,
    started_at=datetime.now(pytz.timezone(TIME_ZONE)),
    no_of_students_at_started=len(channel.members),
    started=True,
  )

  for member in channel.members:
    name = getting_username(member.nick)
    if name[0:2] == "22":
      attendance.append(name)

  registered_students = await sync_to_async(Students.objects.filter
                                            )(registered=True)

  for student in registered_students:

    if student.user.username in attendance:
      present = True
    else:
      present = False
    try:
      student_record = await sync_to_async(Attendance_Student.objects.get)(
        user=student.user,
        session_name=runtime_details.session_name,
        subject=runtime_details.subject)
    except Attendance_Student.DoesNotExist:
      student_record = await sync_to_async(Attendance_Student.objects.create)(
        user=student.user,
        session_name=runtime_details.session_name,
        subject=runtime_details.subject,
        present=present,
        log_on_at=datetime.now(pytz.timezone(TIME_ZONE)))
    print("present marked", student.user.username)
  print(attendance)

  # channnel_name = channel.get_channel(1074002913065717950)


#   # members = channel.members
#   # for member in members:
#   #   print(member.name)

# asyncio.create_task(present_marking())
keep_alive()
client.run(api_key)
