import itertools
import os
import random


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


def find_best_groups(permutations, matrix):
    """Loop through each possible set of groups and calculate its score,
    given the supplied cost matrix.

    :param permutations: A list containing a lists of possible sets of groups
    :param matrix: The cost matrix for pairs of students
    :returns: A list of all possible sets of groups with the lowest score
        out of all possible sets
    """
    best_groups = []
    min_score = 99999
    for set_of_groups in permutations:
        score = 0
        for group in set_of_groups:
            # Generate all pair-combinations of students in each group
            #  and add the cost of that pairing
            group_combinations = itertools.combinations(group, 2)
            for a, b in group_combinations:
                score += int(matrix[a][b])
        # Score now contains the total score for the entire set of groups
        # Only keep sets of groups whose score is <= to the lowest found score
        if score == min_score:
            best_groups.append(set_of_groups)
        elif score < min_score:
            # If new group has lower score:
            #  update min_score
            #  clear best groups, and then add new group
            min_score = score
            best_groups = [set_of_groups]
    return best_groups


def cast_into_chunks(data, chunk_sizes):
    """Loop through list, divide list into list of lists of given sizes.

    :param data: a list of lists or tuples to be divided into sub-groups
    :param chunk_sizes: a list, each element is the size of the sub-groups
    :returns: A list of possible sets of groups,
        each of which is a list (a set of groups) of lists (groups) of students
    """
    # Loop through list of permutations
    for row in data:
        # Convert from tuple to list
        permutation = list(row)
        list_of_groups = []
        # Loop through each listed group size
        for chunk_size in chunk_sizes:
            group = []
            # Pop "chunk_size" number of indices from the front
            #  of the permutation and add to list
            for i in range(chunk_size):
                group.append(permutation.pop(0))
            # Append that chunk to the list of groups
            list_of_groups.append(group)
        yield list_of_groups


class Student:
    """Hold information on a single student"""

    def __init__(self, record, course=None):
        """Load a student record from a comma separated text line

        :param record: a comma separated text line
        """
        if not course:
            x = record.strip().split(",")
            self.index = int(x[0])
            self.firstName = x[1]
            self.lastName = x[2]
            self.history = [int(num) for num in x[3:]]
        else:
            x = record.strip().split(" ")
            self.firstName = x[0]
            self.lastName = x[1]
            self.index = len(course.course_roster)
            self.history = [int(num) for num in "0" * len(course.course_roster)]

    def name(self):
        """Return full name by merging first and last"""
        return self.firstName + " " + self.lastName

    def save_record(self):
        """Return comma separated record ready to be written to save file"""
        history_joined = ",".join([str(x) for x in self.history])
        return ",".join([str(self.index), self.firstName,
                         self.lastName, history_joined])


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
                # Reload course from file, deleting changes
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
        # Expand history for all students in roster
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


class Session:
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


# Run main function
if __name__ == "__main__":
    main()

