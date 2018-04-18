from peewee import *
import os
import datetime
import sys

__location__ = os.path.realpath(
                 os.path.join(os.getcwd(), os.path.dirname(__file__))
               )
db =  SqliteDatabase(os.path.join(__location__, 'db/worklog.db'));

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

def initialize():
    print("initializing ...")
    """create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Employee, Task], safe=True)


def create():
    print("creating")

    employee_name =  "Zev Tovbin"
    employee_username = "ztovbin"

    try:
        newemployee = Employee.get(employee_username = employee_username)
    except DoesNotExist:
        print("employee not found")
        newemployee = Employee(employee_username=employee_username, employee_name=employee_name)
        newemployee.save()

    task = Task(employee=newemployee, title='working with Linux', timespent=40, notes="notes")
    task.save()

def search():
    entries = Task.select().order_by(Task.timestamp.desc())
    for entry in entries:
        print(entry.title)

if __name__ == "__main__":
    initialize()
    create()
    search()
