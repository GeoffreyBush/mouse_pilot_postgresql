import csv

from website.models import Info


def run():
    with open("website/static/mouse_info.csv") as file:
        reader = csv.reader(file)

        Info.objects.all().delete()

        for row in reader:
            print(row)

            info = Info(
                id=row[0],
                note=row[1],
                email_record=row[2],
            )
            info.save()
