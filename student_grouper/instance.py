import os
from course import Course


class Instance:
    """Program session, contains UI methods

    """

    def __init__(self, directory):
        """Initialize new session

        :param directory: the file directory which holds save files
        """
        self.directory = directory

    def main_menu(self):
        """Infinite loop that operates main menu"""
        course = False
        while True:
            if course:
                print(course.desc + " is loaded\n")
            print("1) Load Course")
            print("2) Add Course\n")
            if course:
                print("3) Make Groups")
                print("4) Edit Course\n")
            print("Q) Quit")

            choice = input()

            if choice == "1":
                # Select course
                course = self.choose_course()

            elif choice == "2":
                # Create new course
                while True:
                    # Get course description and generate file name from it
                    desc = input("Enter course description:")
                    file_name = desc.replace(" ", "_") + ".txt"
                    # Check that filename doesn't already exist
                    course_files = [file for file in os.listdir(self.directory)
                                    if file.endswith(".txt")]
                    if file_name not in course_files:
                        # If it doesn't exist, break from loop and create course
                        break
                    else:
                        print("A course with that name already exists."
                              "Please modify the description")

                # Make a new Course from filename and description
                course = Course(self.directory + "/" + file_name, desc)
                # Immediately edit students in course
                course.edit_students()

            elif choice == "3" and course:
                # Make groups from loaded course

                print("Define group by (S)ize or (N)umber?")
                group_by = input().lower().split()[0]
                if group_by == "s":
                    print("Enter group size:")
                elif group_by == "n":
                    print("Enter number of groups")
                group_val = int(input())
                # Make groups
                final_groups = course.make_groups(group_val, group_by)

                # Print names of group members
                for group in final_groups:
                    print(" + ".join(course.indices_to_names(group)))
                break

            elif choice == "4" and course:
                course.edit_students()

            elif choice.lower().startswith("q"):
                # Quit program
                break

    def choose_course(self):
        """UI to choose a course from the save files in the specified directory

        :return: A new Course object generated based on selected file
        """
        # Continue looping until user chooses a class or enters quit
        while True:
            print("Choose a class to load:")
            # Get list of all .txt files in the course directory
            course_file = [file for file in os.listdir(self.directory)
                           if file.endswith(".txt")]

            # Print list of files with their index to allow selection
            for index, file in enumerate(course_file):
                print(str(index) + ") " + file)

            # Get user's choice
            choice = input()

            if choice.startswith("q"):
                quit()
            # If selected index is valid, load the course and return object
            elif int(choice) < len(course_file):
                return Course(self.directory + "/" + course_file[int(choice)])
