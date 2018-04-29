from peewee import *
import os
import datetime


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

db_directory =__location__+"/db/"
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

db = SqliteDatabase(db_directory + "worklog.db")


class Employee(Model):
    """
    Employee model
    """
    employee_username = CharField(unique=True)
    employee_name = CharField()

    class Meta:
        database = db


class Task(Model):
    """
    Task Model - contains Employee as foreign key
    """
    employee = ForeignKeyField(Employee)
    title = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    timespent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def find_employee(employee_username):
    """
    Search for employee in the database
    return Employee found if not return None
    """
    try:
        employee = Employee.get(employee_name=employee_username)
    except DoesNotExist:
        return None
    return employee


def initialize():
    """create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Employee, Task], safe=True)


if __name__ == "__main__":
    initialize()
