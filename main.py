from flask import Flask
from session import *
from course import *
from student import *
from functions import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World THIs is two!'


def main():
    # Create new session
    # noinspection SpellCheckingInspection
    session = Session("classfiles")
    session.main_menu()
    # Select course
    # course = session.choose_course()

    # Make groups
    # final_groups = course.make_groups(4, "s")

    # Print names of group members
    # for group in final_groups:
    #    print(" + ".join(course.indices_to_names(group)))
