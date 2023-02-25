import discord
from Aca_sessions.models import Subjects

INCORRECT_NICKNAME = "Your nickname is incorrect"
REGISTRED = "You are registered"
REGISTRED_ALREADY = "You have already registered"

INCORRECT_REGISTRATION_NUMBER = "Your Registration Number is incorrect"


option_list_of_subjects = [
      discord.SelectOption(
        label=Subjects.CS.label,
        value=Subjects.CS.value,
      ),
      discord.SelectOption(
        label = Subjects.Maths.label,
        value=Subjects.Maths.value,
      ),
      discord.SelectOption(
        label=Subjects.Electrical.label,
        value=Subjects.Electrical.value,
      ),
      discord.SelectOption(
        label = Subjects.Fluid.label,
        value = Subjects.Fluid.value
      ),
      discord.SelectOption(
        label= Subjects.Material.label,
        value = Subjects.Material.value
      ),
      discord.SelectOption(
        label=Subjects.Mechanics.label,
        value=Subjects.Mechanics.value
      ),
    ]