import unittest
from io import StringIO
from employeemenu import EmployeeMenu
from tasksearch import TaskSearch
from mainmenu import MainMenu
from workdbutils import *
from unittest import mock
from mock import patch
import datetime


class TestEmployeeMenu(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        test_db = SqliteDatabase(':memory:')
        Employee._meta.database = test_db
        Task._meta.database = test_db
        test_db.connect()
        test_db.create_tables([Employee, Task], safe=True)

        employee_name = "Ron John"
        employee_username = "rjohn"
        TestEmployeeMenu.addEmployee(employee_name,employee_username)

    @classmethod
    def addEmployee(cls, employee_name, employee_username):
        newemployee = Employee.create(employee_username=employee_username,
                                      employee_name=employee_name)
        newemployee.save()

    @classmethod
    def addTask(cls, employee, task_title, task_timespent, task_notes):
        task = Task(employee=employee, title=task_title,
                    timespent=int(task_timespent), notes=task_notes)
        task.save()




    def test_add_employee(self):

        employee_menu = EmployeeMenu()
        employee_username = "jblack"
        employee_name  = "Jack Black"

        with mock.patch('builtins.input', side_effect=[ employee_username,
                                                        employee_name ,'q']):
            employee_menu.add_employee()

        found_employee = Employee.get(employee_username = employee_username)
        self.assertEqual(found_employee.employee_username, employee_username)
        self.assertEqual(found_employee.employee_name, employee_name)



    def test_add_existing_employee(self):

        employee_menu = EmployeeMenu()
        employee_name = "Ron John"
        employee_username = "rjohn"

        with mock.patch('builtins.input', side_effect=[ employee_username,
                                                        employee_name ,'q']):
            added_successfully = employee_menu.add_employee()

        self.assertFalse(added_successfully)



    @patch('sys.stdout', new_callable=StringIO)
    def test_view_employees(self, mock_stdout):
        employee_name2 = "Ron John"
        employee_username2 = "rjohn"

        employee_username1 = "jblack"
        employee_name1  = "Jack Black"

        employee_menu = EmployeeMenu()
        with mock.patch('builtins.input', side_effect=['q','n','q']):
            employee_menu.view_employees()
        self.assertEqual(len(employee_menu.employees), 3)

        employee = employee_menu.employees[0]
        self.assertEqual(employee.employee_name, employee_name1)
        self.assertEqual(employee.employee_username, employee_username1)

        employee = employee_menu.employees[1]
        self.assertEqual(employee.employee_name, employee_name2)
        self.assertEqual(employee.employee_username, employee_username2)



    def test_delete_employee(self):

        employee_username = "jdoe"
        employee_name = "John Doe"

        TestEmployeeMenu.addEmployee(employee_name,employee_username)

        employee_menu = EmployeeMenu()
        found_employee = Employee.get(employee_username = employee_username)
        with mock.patch('builtins.input', side_effect=[ 'y','q']):
              employee_menu.delete_entry(found_employee)

        with self.assertRaises(DoesNotExist):
             Employee.get(employee_username=employee_username)


    def test_delete_employee_with_task(self):
        employee_menu = EmployeeMenu()
        test_username = "test1"
        TestEmployeeMenu.addEmployee("Test Employee", test_username)
        test_employee = Employee.get(employee_username = test_username)

        task_title = "Testing Task"
        task_timespent = "20"
        task_notes  = "Testing out code"
        TestEmployeeMenu.addTask(test_employee,task_title,task_timespent,
                                 task_notes)

        with mock.patch('builtins.input', side_effect=[ 'y','q']):
            deleted_successfully = employee_menu.delete_entry(test_employee)

        self.assertFalse(deleted_successfully)

    def test_convert_date(self):
        self.assertIsInstance(convertdate("04/25/2018"),datetime.datetime)
        self.assertIsNone(convertdate("13/25/2018"))




class TestTaskSeach(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        test_db = SqliteDatabase(':memory:')
        Employee._meta.database = test_db
        Task._meta.database = test_db
        test_db.connect()
        test_db.create_tables([Employee, Task], safe=True)

        employee_name = "Testing Task"
        employee_username = "test"
        TestEmployeeMenu.addEmployee(employee_name,employee_username)

    @classmethod
    def addEmployee(cls, employee_name, employee_username):
        newemployee = Employee.create(employee_username=employee_username,
                                      employee_name=employee_name)
        newemployee.save()

    @classmethod
    def addTask(cls, employee, task_title, task_timespent, task_notes):
        task = Task(employee=employee, title=task_title,
                    timespent=int(task_timespent), notes=task_notes)
        task.save()

    def test_add_task(self):
        main_menu =  MainMenu()
        test_name = "Testing Task"
        task_title = "Testing Task Title"
        task_timespent = "20"
        task_notes  = "Testing out code"

        prompts = [test_name, task_title, task_timespent, task_notes,'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            added_successfully = main_menu.add_task()
        self.assertTrue(added_successfully)

    def test_add_task_employee_not_found(self):
        main_menu =  MainMenu()
        test_name = "Employee Notfound"
        task_title = "Testing Task Title"
        task_timespent = "20"
        task_notes  = "Testing out code"

        prompts = [test_name, task_title, task_timespent, task_notes,'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            added_successfully = main_menu.add_task()
        self.assertFalse(added_successfully)


    def test_view_tasks(self):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['s','v','q','q']):
            tasksearch_menu.view_entries()
        self.assertEqual(len(tasksearch_menu.entries), 1)


    def test_simple_search(self):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['code','q','q']):
            tasksearch_menu.view_entries( )
        self.assertEqual(len(tasksearch_menu.entries), 1)

    def test_simple_search_notfound(self):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['dog','q','q']):
            tasksearch_menu.simple_search()
        self.assertEqual(len(tasksearch_menu.entries), 0)

    def test_employee_search(self):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['Testing Task',
                                                       'q', 'q']):
            tasksearch_menu.search_by_employee_name()
        self.assertEqual(len(tasksearch_menu.entries), 1)

        with mock.patch('builtins.input', side_effect=['John Doe',
                                                       'q', 'q']):
            tasks_found = tasksearch_menu.search_by_employee_name()
        self.assertFalse(tasks_found)

    def test_date_search(self):
        tasksearch_menu = TaskSearch()
        today_str = datetime.datetime.now().strftime('%m/%d/%Y')
        with mock.patch('builtins.input', side_effect=[today_str,'q','q','q']):
            tasksearch_menu.search_by_taskdate()
        self.assertEqual(len(tasksearch_menu.entries), 1)





if __name__ == "__main__":
     print("hi")
     unittest.main()
