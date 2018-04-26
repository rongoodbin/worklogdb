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

if __name__ == "__main__":
    initialize()
    #create()
    search()
