from employeemenu import *
from workdbutils import *


class TaskSearch():

    def __init__(self):

        self.entries = None
        self.menu = OrderedDict([
            ('v', self.view_entries),
            ('s', self.simple_search),
            ('l', self.search_by_employee_list),
            ('n', self.search_by_employee_name),
            ('t', self.search_by_timespent),
            ('d', self.search_by_taskdate),
            ('r', self.search_by_daterange)

        ])

    def entries_count(self):
        return len(self.entries)

    def view_entries(self, **kwargs):
        """view previous entries """
        self.entries = None
        if "employee" in kwargs and kwargs['employee']:
            self.entries = Task.select().where(
                Task.employee == kwargs['employee']) \
                .order_by(Task.id.asc())
        elif "time_spent" in kwargs:
            timespent = int(kwargs['time_spent'])
            self.entries = Task.select().where(Task.timespent == timespent) \
                .order_by(Task.id.asc())
        elif "entry_date" in kwargs:
            sdate = kwargs["entry_date"]
            print("entry_date:" + str(sdate))
            self.entries = Task.select().where(
                Task.timestamp.year == sdate.year \
                and Task.timestamp.month == sdate.month \
                and Task.timestamp.day == sdate.day) \
                .order_by(Task.id.asc())
        elif "date_range" in kwargs:
            startdate = kwargs["date_range"][0]
            enddate = kwargs["date_range"][1]
            self.entries = Task.select().where(Task.timestamp.between(
                startdate, enddate))
        else:
            self.entries = Task.select().order_by(Task.id.asc())

        if "search_query" in kwargs:
            self.entries = self.entries.where(Task.title.contains
                                              (kwargs['search_query']) |
                                              Task.notes.contains(
                                                  kwargs['search_query'])
                                              )

        position = 0
        if self.entries:
            clear()
            while True:
                entry = self.entries[position]
                timestamp = entry.timestamp.strftime('%A %B %d %Y %I:%M')

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

                next_action = input("Action [NPEqd] ").lower().strip()

                if next_action.lower() == "n":
                    position += 1
                    position = position % len(self.entries)
                    clear()
                    continue
                if next_action.lower() == "p":
                    position -= 1
                    position = position % len(self.entries)
                    clear()
                    continue
                if next_action == "q":
                    clear()
                    break
                if next_action == "e":
                    clear()
                    self.taskedit(entry)
                if next_action == 'd':
                    self.delete_entry(entry)
                    break
                clear()
        else:
            print("No tasks found.")

    def taskedit(self, task):

        timestamp = task.timestamp.strftime('%A %B %d %Y %I:%M')

        while True:
            print("Task Date:" + timestamp)
            response = input("Enter new value or enter to leave as is: ")
            if response != "":
                newtimestamp = convertdate(response)
                if newtimestamp:
                    task.timestamp = newtimestamp
                    break
                else:
                    print("Date format is incorrect")
            else:
                break

        print("Task Title:" + task.title)
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            task.title = response

        print("Time Spent:" + str(task.timespent))
        while True:
            response = input("Enter new value or enter to leave as is: ")
            if response != '':
                if not response.isdigit():
                    print("Need an integer value!")
                    continue
                if response != "":
                    task.timespent = int(response)
                    break
            else:
                break

        print("Notes:" + str(task.notes))
        response = input("Enter new value or enter to leave as is: ")
        if response != "":
            task.notes = response

        task.save()

    def delete_entry(self, entry):
        if input("Are you sure? [yN] ").lower() == 'y':
            entry.delete_instance()
            print("Entry is deleted")
            return True

    def search_by_timespent(self):
        """Search by time spent on task"""
        self.view_entries(time_spent=input("TimeSpent: "))

    def simple_search(self):
        """Simple search of work logs"""
        self.view_entries(search_query=input("Search query: "))

    def search_by_taskdate(self):
        """search by task entry date"""
        datefromuser = convertdate(input("Please use DD/MM/YYYY: "))
        if datefromuser:
            print(datefromuser)
            self.view_entries(entry_date=datefromuser)

    def search_by_daterange(self):
        """search by date range"""
        startdate = convertdate(input("Enter a start date( DD/MM/YYYY: "))
        enddate = convertdate(input("Enter an end date( DD/MM/YYYY: "))

        if startdate and enddate:
            self.view_entries(date_range=[startdate, enddate])

    def search_by_employee_name(self):
        """Search for tasks by employee name"""
        employee_name = input("Enter partial name:").strip()
        self.search_by_employee_list(employee_name=employee_name)

    def search_by_employee_list(self, employee_name=None):
        """find by employee list"""
        employee_map = {}
        employees = Employee.select()
        if employee_name:
            employees = employees.where(
                Employee.employee_username.contains(employee_name) |
                Employee.employee_name.contains(employee_name)
            )

        for index, employee in enumerate(employees):
            employee_name = employee.employee_name
            employee_map[index + 1] = employee
            print("{0}) {1}".format(index + 1, employee_name))
        selection = input("Please select an employee by index: ")
        try:
            self.view_entries(employee=employee_map[int(selection)])
        except ValueError:
            print("Invalid selection")

    def menu_loop(self):
        """show the menuu"""
        print("Task Search Menu:" + os.linesep)
        choice = None
        while choice != 'q':
            print("Enter q to quit")
            for key, value in self.menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input('Action: ').lower().strip()
            if choice in self.menu:
                self.menu[choice]()
