import csv

from website.models import Mice


# File needs to be updated to reflect current Mice model
def run():
    with open("website/static/mouse_stocks.csv") as file:
        reader = csv.reader(file)

        Mice.objects.all().delete()

        for row in reader:
            print(row)

            mice = Mice(
                id=row[0],
                clippedDate=row[1],
                genotypedOrNot=row[2],
                genotyper=row[3],
                earmark=row[4],
                sex=row[5],
                box=row[6],
                dob=row[7],
                mother=row[8],
                father=row[9],
                strain=row[10],
                cre1=row[11],
                cre2=row[12],
                gasp=row[13],
            )
            mice.save()
