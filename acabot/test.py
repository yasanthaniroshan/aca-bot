from django.conf import settings
import django,csv
from acabot.settings import DATABASES,INSTALLED_APPS

settings.configure(DATABASES=DATABASES,INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from Users.models import User,Students


with open("newStudents.csv") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for line in csv_reader:
        name= line['Name'].strip().split(" ")
        if len(name) ==  1:
            firstname = name[0].split(".")[-1]
            lastname = ""
        elif len(name) >= 2 :
            firstname = name[0].split(".")[-1]
            lastname = " ".join(name[1:])
        if len(line['District Rank']) == 1:
            username = "22"+"00"+ line['District Rank']
        elif len(line['District Rank']) == 2:
            username = "22"+"0"+line['District Rank']
        elif len(line['District Rank']) == 3:
            username = "22"+line['District Rank'] 
        if line['Email address'] != "":
            User.objects.create(
                username = username,
                first_name = firstname,
                last_name = lastname,
                email = line['Email address'],
                )
        else:
            User.objects.create(
                username = username,
                first_name = firstname,
                last_name = lastname,
                )
        
        Students.objects.create(
            user = User.objects.get(username=username),
            island_rank = line['Island Rank'],
            school = line['School'],
            whatsapp_number = line['Whatsapp Number'],
        )

        print(username,name)