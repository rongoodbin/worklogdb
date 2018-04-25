from collections import OrderedDict
from employeemenu import *
from workdbutils import *


class EmployeeMenu:

    def __init__(self):

        self.menu = OrderedDict([
            ('a', self.add_employee),
            ('v', self.view_employees),
            ('s', self.search_employees)
        ])

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
            return False
        print("New employee has been added successfully.")
        return True

    def view_employees(self, search_query=None):
        """view employees"""
        self.employees = Employee.select().order_by(Employee.employee_name.asc())
        if search_query:
            self.employees = employees.where(
                           Employee.employee_username.contains(search_query) |
                           Employee.employee_name.contains(search_query)
                         )
        position = 0
        if self.employees:
            clear()
            while True:
                employee = self.employees[position]
                #timestamp = entry.timestamp.strftime('%A %B %d %Y %I:%M')
                #print(timestamp)
                employee_name = employee.employee_name
                print('=' *  len(employee_name))
                print("Employee Username: {0}".format(
                              employee.employee_username)
                     )
                print("Employee Name: {0}".format(employee.employee_name))
                print("\n\n" + "=" * len(employee_name))
                print('N) next entry')
                print('d) delete entry')
                print('q) return to main menu')
                next_action = input("Action [NPqd] ").lower().strip()
                if next_action.lower() == "n":
                    position += 1
                    position = position % len(employees)
                    clear()
                    continue
                if next_action.lower() == "p":
                    position -= 1
                    position = position % len(employees)
                    clear()
                    continue
                if next_action == "q":
                    clear()
                    break
                if next_action == 'd':
                    self.delete_entry(employee)
                    break
                clear()

    def delete_entry(self, employee):
        if input("Are you sure? [yN] ").lower() == 'y':
            task_count = Task.select().where(Task.employee == employee).count()
            #print("task_count="+ str(task_count))
            if  task_count > 0:
                cantDeleteEmployee()
                return False
            employee.delete_instance()
            print("Employee is deleted")
            return True

    def search_employees(self):
        """search employees"""
        self.view_employees(input("Search employee: "))

    def menu_loop(self):
        """show the menuu"""
        print("Employee management" + os.linesep)
        choice = None
        while choice != 'q':
            clear
            print("Enter q to quit")
            for key, value in self.menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input('Action: ').lower().strip()
            if choice in self.menu:
                self.menu[choice]()
