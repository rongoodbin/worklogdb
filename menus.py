from models import *
from collections import OrderedDict
from workdbutils import *
from peewee import IntegrityError
import os


class EmployeeMenu():


    def __init__(self):
        pass

    def find_employee(self,employee_username):
        try:
            employee = Employee.get(employee_username=employee_username)
        except DoesNotExist:
            return  None
        return employee



class MainMenu():

    def __init__(self):

        self.menu = OrderedDict([
            ('a', self.add_task),
            ('e', self.add_employee),
            ('v', self.view_entries),
            ('s', self.search_entries)
        ])
        self.employee_menu = EmployeeMenu()

    def add_employee(self):
        """add a new employee to the task system"""
        employee_username = input("Enter new employee userid: ")
        employee_name = input("Enter new employee full name: ")
        newemployee = Employee(employee_username=employee_username,
                               employee_name=employee_name)
        try:
            newemployee.save()
        except IntegrityError:
            print("Employee is already present in the system.")
            return
        print("New employee has been added successfully.")

    def add_task(self):
        """add a new task entry to the system"""
        print("Task entry:")
        employee_username = input("Employee username:")
        employee = self.employee_menu.find_employee(employee_username)
        task_title = input("Task title:")
        task_timespent = input("Time spent on Task(minutes):")
        task_notes = input("Task Notes:")

        if input("Save task? [Yn] ").lower() != 'n':
                print("saved successfully")

        task = Task(employee=employee, title=task_title,
                    timespent=int(task_timespent), notes=task_notes)
        task.save()
        print("Task saved !")



    def view_entries(self, search_query=None):
        """view previous entries """
        entries = Task.select().order_by(Task.id.asc())
        if search_query:
            entries = entries.where(Task.title.contains(search_query) |
                                    Task.notes.contains(search_query)
                                    )
        position = 0
        if entries:
            while True:
                entry  = entries[position]
                timestamp = entry.timestamp.strftime('%A %B %d %Y %I:%M')
                print(timestamp)
                print('=' * len(timestamp))
                print("Task ID: {0}".format(entry.id))
                print("Task Title: {0}".format(entry.title))
                print("Employee: {0}".format(entry.employee.employee_name))
                print("Task Entry time: {0}".format(timestamp))
                print("Task time spent: {0}".format(entry.timespent))
                print("Task Notes: {0}".format(entry.notes))

                print("\n\n" + "=" * len(timestamp))
                print('N) next entry')
                print('d) delete entry')
                print('q) return to main menu')

                next_action = input("Action [NPqd] ").lower().strip()

                if next_action.lower() == "n":
                    position += 1
                    position = position % len(entries)
                    clear()
                    continue
                if next_action.lower() == "p":
                    position -= 1
                    position = position % len(entries)
                    clear()
                    continue
                if next_action == "q":
                    clear()
                    break
                if next_action == 'd':
                    self.delete_entry(entry)
                    break


                    
    def delete_entry(self,entry):
        if input("Are you sure? [yN] ").lower() == 'y':
            entry.delete_instance()
            print("Entry is deleted")
            return True

    def search_entries(self):
       """Search work logs for a string"""
       self.view_entries(input("Search query: "))

    def menu_loop(self):
        """show the menuu"""
        print("Welcome to the employee Taskmanagment system."+os.linesep)
        choice = None
        while choice != 'q':
            clear
            print("Enter q to quit")
            for key, value in self.menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input('Action: ').lower().strip()
            if choice in self.menu:
                self.menu[choice]()