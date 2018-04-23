from unittest import TestCase
from peewee import *
from models import Task, Employee, db
from mainmenu import MainMenu
from unittest import mock


class TestMainMenu(TestCase):


    def setUp(self):
        self.test_db = SqliteDatabase(':memory:')
        Employee._meta.database = self.test_db
        Task._meta.database = self.test_db
        self.test_db.connect()
        print("connecting to database ...")
        self.test_db.create_tables([Employee, Task], safe=True)

    def test_create_employee(self):

        employee_name = "Jack Black"
        employee_username = "jblack"

        newemployee = Employee.create(employee_username=employee_username,
                                      employee_name=employee_name)
        newemployee.save()
        print(newemployee.employee_name)
        print(newemployee.employee_username)
        self.assertIsNotNone(newemployee)

    def test_add_employee(self):
        main_menu = MainMenu()
        with mock.patch('builtins.input', side_effect="rjohn4552"):
            main_menu.add_task()
            mock.patch('builtins.input', side_effect="Ron John")
            mock.patch('builtins.input', side_effect="Testing Task System")
            mock.patch('builtins.input', side_effect="10")
            mock.patch('builtins.input', side_effect="Some Notes")
            mock.patch('builtins.input', side_effect="Y")
            mock.patch('builtins.input', side_effect="q")

        #findEmployee = Employee.get(employee_username = "rjohn4552")
        #self.assertIsNotNone(findEmployee)


    def tearDown(self):
        pass