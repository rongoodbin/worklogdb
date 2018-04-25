from peewee import *
import os
import datetime



__location__  = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
            )

db = SqliteDatabase(os.path.join(__location__, 'db/worklog.db'))



class Employee(Model):
    employee_username = CharField(unique=True)
    employee_name = CharField()

    class Meta:
        database = db

class Task(Model):
     employee  = ForeignKeyField(Employee)
     title = CharField()
     timestamp  =  DateTimeField(default=datetime.datetime.now)
     timespent = IntegerField(default=0)
     notes     = BlobField()

     class Meta:
        database = db


def find_employee(employee_username):
        try:
            employee = Employee.get(employee_name=employee_username)
        except DoesNotExist:
            return  None

        return employee



def initialize():
    """create the database and the table if they don't exist"""
    print("initializing ...")
    db.connect()
    print("connecting to database ...")
    db.create_tables([Employee, Task], safe=True)

"""
def create():
    print("creating")

    employee_name =  "Jack Black"
    employee_username = "jblack"

    try:
        newemployee = Employee.get(employee_username = employee_username)
    except DoesNotExist:
        print("employee not found")
        newemployee = Employee(employee_username=employee_username, employee_name=employee_name)
        newemployee.save()

    task = Task(employee=newemployee, title='acting in a movie', timespent=500, notes="movie is goign to rock")
    task.save()

def search():
    #entries = Task.select().order_by(Task.timestamp.desc())
    entries = Task.select()
    for entry in entries:
        print("{0}-{1}-{2}".format(entry.timestamp.day, entry.timestamp.month, entry.timestamp.year))


    sdate = datetime.datetime.strptime("04/19/2018", '%m/%d/%Y')

    print("{0}/{1}/{2}".format(sdate.month,sdate.day,sdate.year))
    entries = Task.select().where(Task.timestamp.year == sdate.year and Task.timestamp.month == sdate.month and Task.timestamp.day == sdate.day)\
                                 .order_by(Task.id.asc())
    print(len(entries))
    for entry in entries:
        print(entry.timestamp)
"""

if __name__ == "__main__":
    initialize()
    #create()
    search()
