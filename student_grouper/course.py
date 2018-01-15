import random
from student import Student
from functions import *


class Course:
    """Course objects hold all student objects loaded from one save file"""

    def __init__(self, filename, desc=""):
        """
        Create a new Course object:
         1) by either loading a saved file (if filename exists)
         2) or by creating a new one, which will be saved as filename

        :param filename: Name for the save file for this course
        :param [desc]: define course description when creating new course
        """
        self.course_roster = []
        self.desc = desc
        self.filename = filename

        try:
            fp = open(file=filename)
            fp.close()
            self.load_file(filename)
        except FileNotFoundError:
            print("New course created!")
            self.save()

    def load_file(self, filename):
        """Load save file and generate new course object

        :param filename: filename for save file to be loaded
        """
        with open(file=filename) as file:
            for record in file:
                if record.startswith("#"):
                    self.desc = record.strip().strip("#")
                else:
                    student = Student(record)
                    self.course_roster.append(student)

    def save(self):
        """Write course object to save file.

        Each course object save the filename from the file it was loaded from
        and then saves itself to that same file
        """
        # Writes the Course object to a save file
        with open(file=self.filename, mode="w") as outfile:
            outfile.writelines("#" + self.desc + "\n")
            for student in self.course_roster:
                outfile.writelines(student.save_record() + "\n")

    def return_students(self):
        """Make list of (index, full names) of all students in course

        :return: List of tuples, each contains 1 student index + full name
        """
        students = []
        for student in self.course_roster:
            # Make tuple of index + fullname and add to list
            students.append((student.index, student.name()))
        return students

    def edit_students(self):
        """Menu for editing students.

        :return:
        """
        while True:
            choice = input("1) Add Student\n"
                           "2) List Students\n"
                           "3) Remove Students\n\n"
                           "S) Save Changes\n"
                           "C) Cancel Changes\n")

            if choice == "1":
                # Add Students repeatedly until user breaks
                while True:
                    student = input("Enter Student Name (or Q to finish): ")
                    if student.lower() == "q":
                        break
                    else:
                        self.add_student(student)

            if choice == "2":
                # Print student names
                [print(student[1]) for student in self.return_students()]

            if choice == "3":
                # Print student names with indices
                [print(student[0] + ") " + student[1])
                 for student in self.return_students()]
                # Prompt for indices to delete
                delete = input("Enter indices separated by commas to delete"
                               "(or Q to finish): ")

                if delete.lower() == "q":
                    break
                else:
                    # Split list on comma, delete all students listed
                    for index in delete.split(","):
                        self.remove_student(index)

            if choice.lower() == "s":
                # Save course to file with changes
                self.save()
                break
            if choice.lower() == "c":
                # Clear course_roster and Reload course from file
                self.course_roster = []
                self.load_file(self.filename)
                break

    def add_student(self, student):
        """Generate new student from name and add to course_roster

        :param student: Student name: "First Last"
        """
        # Generate new student
        new_student = Student(student, course=self)
        # Add to roster
        self.course_roster.append(new_student)
        # Expand history for all students in roster by adding a new column
        #  containing 0 to all students
        for student in self.course_roster:
            student.history.append("0")

    def remove_student(self, student):
        pass

    def student_indices(self):
        """Return list containing indices of all students

        :return: list containing indices of all students
        """
        return [student.index for student in self.course_roster]

    def gen_history_matrix(self):
        """Make matrix showing # times each student was paired with each other

        :return: n x n matrix (n = number of students in course),
        matrix[m][n] = the number of times students m and n have worked together
        """
        matrix = []
        for student in self.course_roster:
            matrix.append(student.history)
        return matrix

    def indices_to_names(self, group):
        """Return list of names of students from a list of indices

        :param group: A list of indices for group members
        :return: A list of the full names of students in that group
        """
        names = []
        for index in group:
            names.append(self.course_roster[index].name())
        return names

    def group_list_by_size(self, group_size):
        """Returns list of the group sizes to be generated, based on group SIZE

        If class doesn't divide evenly, a new, smaller group will be created
         unless only there is only one remainder,
         or the new group will be 2+ smaller than the desired group
         in which case the remainder will be divided between existing groups
        :param group_size: The desired size of the groups
        :return: List containing the sizes of the groups to be made
        """
        class_size = len(self.course_roster)
        list_of_group_sizes = []
        # Integer division, floor
        num_groups = class_size // group_size
        remainder = class_size % group_size
        for i in range(num_groups):
            list_of_group_sizes.append(group_size)
        if remainder == 1 or group_size-remainder > 1:
            for i in range(remainder):
                list_of_group_sizes[i] += 1
        else:
            list_of_group_sizes.append(remainder)
        return list_of_group_sizes

    def group_list_by_number(self, num_groups):
        """Returns list of the group sizes to be generated, based on # of groups

        If class doesn't divide evenly, it will make groups larger
        :param num_groups: The desired number of groups
        :return: List containing the sizes of the groups to be made
        """
        class_size = len(self.course_roster)
        list_of_group_sizes = []
        # Integer division, floor
        group_size = class_size // num_groups
        remainder = class_size % num_groups
        for i in range(num_groups):
            list_of_group_sizes.append(group_size)
        for i in range(remainder):
            list_of_group_sizes[i] += 1
        return list_of_group_sizes

    def make_groups(self, group_val, group_by):
        """Make groups of students with lowest possible cost

        Can either generate groups by size or number of groups.
        Picks optimal group based on this course's gen_history_matrix() method
        If multiple sets of groups have equal cost, pick one at random

        :param group_val: Either the desired SIZE of group or NUMBER of groups
        :param group_by: If "s" use group_list_by_size, if "n" use ..._by_number
        :return: List of groups, each is a list of indices for its members
        """
        # Get matrix of cost
        matrix = self.gen_history_matrix()

        group_sizes = []
        if group_by.startswith("s"):
            group_sizes = self.group_list_by_size(group_val)
        elif group_by.startswith("n"):
            group_sizes = self.group_list_by_number(group_val)

        # Generate all possible permutations of students
        pair_permutations = itertools.permutations(self.student_indices())

        # Cut those permutations into groups of specified sizes
        grouped_permutations = cast_into_chunks(pair_permutations, group_sizes)

        # Find all groups with the lowest possible score
        best_groups = find_best_groups(grouped_permutations, matrix)

        # Randomly choose one set of groups from the best groups
        return random.choice(best_groups)
