from flask import Flask, session, redirect, url_for
from instance import *
from course import *
from student import *
from functions import *

app = Flask(__name__)


@app.route('/')
def index():
    if username in session:

    else:


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

def main():
    # Create new instance
    # no inspection SpellCheckingInspection
    instance = Instance("classfiles")
    instance.main_menu()
    # Select course
    # course = instance.choose_course()

    # Make groups
    # final_groups = course.make_groups(4, "s")

    # Print names of group members
    # for group in final_groups:
    #    print(" + ".join(course.indices_to_names(group)))
