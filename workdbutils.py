from models import *


def cantDeleteEmployee():
    showUser = "Not able to delete as there are tasks associated" \
               " with employee!"
    print(showUser)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def convertdate(datestr):
    try:
        return datetime.datetime.strptime(datestr, '%m/%d/%Y')
    except ValueError:
        return None
