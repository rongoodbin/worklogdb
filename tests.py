import unittest
from unittest import mock
from io import StringIO

from employeemenu import EmployeeMenu
from tasksearch import TaskSearch
from mainmenu import MainMenu
from workdbutils import *


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
        test_employee = Employee.create(employee_username=employee_username,
                                        employee_name=employee_name)
        test_employee.save()

        task_title = "Testing Task Title1"
        task_timespent = "10"
        task_notes = "Testing out code!"

        task = Task(employee=test_employee, title=task_title,
                    timespent=int(task_timespent), notes=task_notes)
        task.save()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_add_employee(self, mock_stdout):
        employee_menu = EmployeeMenu()
        employee_username = "jblack"
        employee_name = "Jack Black"

        with mock.patch('builtins.input', side_effect=[employee_username,
                                                       employee_name, 'q']):
            employee_menu.add_employee()

        found_employee = Employee.get(employee_username=employee_username)
        self.assertEqual(found_employee.employee_username, employee_username)
        self.assertEqual(found_employee.employee_name, employee_name)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_add_existing_employee(self, mock_stdout):
        employee_menu = EmployeeMenu()
        employee_name = "Ron John"
        employee_username = "rjohn"
        with mock.patch('builtins.input', side_effect=[employee_username,
                                                       employee_name, 'q']):
            added_successfully = employee_menu.add_employee()

        self.assertFalse(added_successfully)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_find_employee(self, mock_stdout):
        employee_menu = EmployeeMenu()
        employee_username = "rjohn"
        with mock.patch('builtins.input', side_effect=[employee_username,
                                                       'q', 'q', 'q']):
            employee_menu.search_employees()
        self.assertEqual(len(employee_menu.employees), 1)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_employees(self, mock_stdout):
        employee_name2 = "Ron John"
        employee_username2 = "rjohn"

        employee_username1 = "jblack"
        employee_name1 = "Jack Black"

        employee_menu = EmployeeMenu()
        with mock.patch('builtins.input', side_effect=['q', 'n', 'q']):
            employee_menu.view_employees()
        self.assertEqual(len(employee_menu.employees), 2)

        employee = employee_menu.employees[0]
        self.assertEqual(employee.employee_name, employee_name1)
        self.assertEqual(employee.employee_username, employee_username1)

        employee = employee_menu.employees[1]
        self.assertEqual(employee.employee_name, employee_name2)
        self.assertEqual(employee.employee_username, employee_username2)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_delete_employee(self, mock_stdout):
        employee_username = "jmith"
        employee_name = "Jane Smith"

        new_employee = Employee.create(employee_username=employee_username,
                                       employee_name=employee_name)

        new_employee.save()

        employee_menu = EmployeeMenu()
        found_employee = Employee.get(employee_username=employee_username)
        with mock.patch('builtins.input', side_effect=['y', 'q']):
            employee_menu.delete_entry(found_employee)

        with self.assertRaises(DoesNotExist):
            Employee.get(employee_username=employee_username)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_delete_employee_with_task(self, mock_stdout):
        employee_menu = EmployeeMenu()

        employee = Employee.get(employee_username="rjohn")

        with mock.patch('builtins.input', side_effect=['y', 'q']):
            deleted_successfully = employee_menu.delete_entry(employee)
        self.assertFalse(deleted_successfully)

    def test_convert_date(self):
        self.assertIsInstance(convertdate("04/25/2018"), datetime.datetime)
        self.assertIsNone(convertdate("13/25/2018"))


class TestTaskSeach(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_db = SqliteDatabase(':memory:')
        Employee._meta.database = test_db
        Task._meta.database = test_db
        test_db.connect()
        test_db.create_tables([Employee, Task], safe=True)

        employee_name = "John Doe"
        employee_username = "test"
        test_employee = Employee.create(employee_username=employee_username,
                                        employee_name=employee_name)
        test_employee.save()
        task_title = "Testing Task Title1"
        task_timespent = "10"
        task_notes = "Testing !"
        task = Task(employee=test_employee, title=task_title,
                    timespent=int(task_timespent), notes=task_notes)
        task.save()

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_add_task(self, mock_stdout):
        # Test adding task with a date provided
        main_menu = MainMenu()
        test_name = "John Doe"
        task_title = "Testing Task Title2"
        task_timespent = "30"
        task_notes = "coding!"
        datestr = "03/18/1981"

        prompts = [test_name, datestr, task_title, task_timespent,
                   task_notes, 'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            added_successfully = main_menu.add_task()
        self.assertTrue(added_successfully)

        # test adding task without date
        task_title = "Testing Task Title3"
        prompts = [test_name, "", task_title, task_timespent,
                   task_notes, 'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            added_successfully = main_menu.add_task()
        self.assertTrue(added_successfully)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_add_task_employee_not_found(self, mock_stdout):
        main_menu = MainMenu()
        test_name = "Employee Notfound"
        task_title = "Testing Task Title"
        task_timespent = "30"
        task_notes = "Testing out code"

        prompts = [test_name, " ", task_title, task_timespent,
                   task_notes, 'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            added_successfully = main_menu.add_task()
        self.assertFalse(added_successfully)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_tasks(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input',
                        side_effect=['s', 'v', 'n', 'p', 'q', 'q']):
            tasksearch_menu.view_entries()
        self.assertEqual(tasksearch_menu.entries_count(), 3)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_simple_search(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['coding', 'q', 'q']):
            tasksearch_menu.simple_search()
        self.assertEqual(tasksearch_menu.entries_count(), 2)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_simple_search_notfound(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['dog', 'q', 'q']):
            tasksearch_menu.simple_search()
        self.assertEqual(tasksearch_menu.entries_count(), 0)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_employee_search(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input', side_effect=['John',
                                                       '1', 'q', 'q', 'q']):
            tasksearch_menu.search_by_employee_name()
        self.assertEqual(tasksearch_menu.entries_count(), 3)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_timespent_search(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        with mock.patch('builtins.input',
                        side_effect=['10', 'q', 'q', 'q']):
            tasksearch_menu.search_by_timespent()
        self.assertEqual(tasksearch_menu.entries_count(), 1)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_date_search(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        today_str = datetime.datetime.now().strftime('%m/%d/%Y')
        with mock.patch('builtins.input',
                        side_effect=[today_str, 'q', 'q', 'q']):
            tasksearch_menu.search_by_taskdate()
        self.assertEqual(tasksearch_menu.entries_count(), 2)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_daterange_search(self, mock_stdout):
        tasksearch_menu = TaskSearch()
        startdate = "03/18/1980"
        enddate = "03/18/1981"
        prompts = [startdate, enddate, 'q', 'q', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            tasksearch_menu.search_by_daterange()
        self.assertEqual(tasksearch_menu.entries_count(), 1)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_delete_task(self, mock_stdout):
        main_menu = MainMenu()
        test_name = "John Doe"
        task_title = "Testing Task To be deleted"
        task_timespent = "1"
        task_notes = "to be deleted"
        datestr = "07/04/1776"

        prompts = [test_name, datestr, task_title, task_timespent,
                   task_notes, 'y', 'q']
        with mock.patch('builtins.input', side_effect=prompts):
            main_menu.add_task()

        task_search = TaskSearch()
        prompts = ["07/04/1776", 'd','y','q','q']
        with mock.patch('builtins.input', side_effect=prompts):
              task_search.search_by_taskdate()

        sdate = convertdate("07/04/1976")
        tasks = Task.select().where(
                      Task.timestamp.year == sdate.year \
                      and Task.timestamp.month == sdate.month \
                      and Task.timestamp.day == sdate.day)

        self.assertEquals(len(tasks), 0)



    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_menu_loop(self, mock_stdout):
        main_menu = MainMenu()
        with mock.patch('builtins.input',
                        side_effect=['s','q','q']):
             return_value = main_menu.menu_loop()
        self.assertTrue(return_value)


if __name__ == "__main__":
    unittest.main()
