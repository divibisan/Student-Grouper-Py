from student_grouper import app
from flask import render_template
# from student_grouper import instance
# from student_grouper import course
# from student_grouper import student
# from student_grouper import functions


@app.route('/')
def index():
    return render_template("index.html")


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