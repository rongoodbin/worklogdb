from collections import OrderedDict
from employeemenu import EmployeeMenu
from tasksearch import TaskSearch
from workdbutils import *


class MainMenu:

    def __init__(self):

        self.menu = OrderedDict([
            ('a', self.add_task),
            ('e', self.employee_management),
            ('s', self.task_search)

        ])

    def employee_management(self):
        """Employee Managment"""
        employee_menu = EmployeeMenu()
        employee_menu.menu_loop()

    def add_task(self):
        """add a new task entry to the system"""
        print("Task entry:")
        employee_name = input("Employee name:")
        employee = find_employee(employee_name)
        if employee:

            while True:
                 task_date_str = input("Task Date (MM/DD/YYYY) or return for today:")
                 if task_date_str == '':
                     task_date = None
                     break
                 task_date = convertdate(task_date_str)
                 if task_date is None:
                     print("Please enter a valid date (MM/DD/YYYY)")
                 else:
                     break

            while True:
                 task_title = input("Task title:")
                 if task_title:
                     break
                 print("You need to enter a task title")

            while True:
                task_timespent = input("Time spent on Task(minutes):")
                if task_timespent == "" or not task_timespent.isdigit():
                    print("Please enter a valid number value for time spent !")
                else:
                    break

            task_notes = input("Task Notes:")
            if input("Save task? [Yn] ").lower() != 'n':
                if task_date:
                    task = Task(employee=employee, timestamp=task_date,
                                title=task_title,
                                timespent=int(task_timespent),
                                notes=task_notes)
                else:
                    task = Task(employee=employee, title=task_title,
                                timespent=int(task_timespent),
                                notes=task_notes)
                task.save()
                print("Task saved !")
                return True
        else:
            print("Employee not found!")
            return False

    def task_search(self):
        """Search for tasks"""
        clear()
        tasksearch = TaskSearch()
        tasksearch.menu_loop()

    def menu_loop(self):
        """show the menuu"""
        print("Welcome to the employee Taskmanagment system." + os.linesep)
        choice = None
        while choice != 'q':
            clear()
            print("Enter q to quit")
            for key, value in self.menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input('Action: ').lower().strip()
            if choice in self.menu:
                self.menu[choice]()
        return True
