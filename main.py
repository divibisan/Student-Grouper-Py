import itertools
import os
import random


def main():
    # Create new session
    # noinspection SpellCheckingInspection
    session = Session("classfiles")

    # Select course
    course = session.choose_course()

    # Make groups
    final_groups = course.make_groups(3, "n")

    # Print names of group members
    for group in final_groups:
        print(" + ".join(course.indices_to_names(group)))


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
                score += matrix[a][b]
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

    def __init__(self, record):
        """Load a student record from a comma separated text line

        :param record: a comma separated text line
        """
        x = record.strip().split(",")
        self.index = int(x[0])
        self.firstName = x[1]
        self.lastName = x[2]
        self.history = [int(num) for num in x[3:]]

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

    def __init__(self, filename):
        """Load save file and generate new course object

        :param filename: filename for save file
        """
        self.filename = filename
        self.course_roster = []
        self.desc = ""
        with open(file=filename) as class_file:
            for record in class_file:
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

        If class doesn't divide evenly, it will make groups larger
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
        for i in range(remainder):
            list_of_group_sizes[i] += 1
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

    def choose_course(self):
        """UI to choose a course from the save files in the specified directory

        :return: A new Course object generate based on selected file
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

