import itertools
import os
import random


def main():
    # Create new session
    session = Session("classfiles")

    # Select course
    course = session.choose_course()

    # Make groups
    final_groups = course.make_groups(3, "n")

    # Print names of group members
    for group in final_groups:
        print(" + ".join(course.indices_to_names(group)))


def find_best_groups(permutations, matrix):
    # Loop through each possible set of groups and calculate its score
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


def sub_groups(pair, pairs):
    a, b = pair
    return [(c, d) for c, d in pairs if c != a and c != b and d != a and d != b]


class Student:
    def __init__(self, record):
        x = record.strip().split(",")
        self.index = int(x[0])
        self.firstName = x[1]
        self.lastName = x[2]
        self.history = [int(num) for num in x[3:]]

    def name(self):
        return self.firstName + " " + self.lastName

    def save_record(self):
        # Generates comma separated record ready to be written to save file
        history_joined = ",".join([str(x) for x in self.history])
        return ",".join([str(self.index), self.firstName,
                         self.lastName, history_joined])


class Course:
    def __init__(self, filename):
        # Generates a new Course object from a save file
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
        # Writes the Course object to a save file
        with open(file=self.filename, mode="w") as outfile:
            outfile.writelines("#" + self.desc + "\n")
            for student in self.course_roster:
                outfile.writelines(student.save_record() + "\n")

    def print_students(self):
        for student in self.course_roster:
            print(student.index, student.name())

    def student_indices(self):
        return [student.index for student in self.course_roster]

    def gen_pairs(self):
        # Returns a list of all possible pairs of students in the class by index
        indices = [student.index for student in self.course_roster]
        # return all unique pairs, order doesn't matter (a,b = b,a)
        #  excludes a-a pairs
        #  and b-a pairs if a-b has already been added
        return [pair for pair in itertools.product(indices, repeat=2)
                if pair[0] < pair[1]]

    def gen_history_matrix(self):
        matrix = []
        for student in self.course_roster:
            matrix.append(student.history)
        return matrix

    def indices_to_names(self, group):
        names = []
        for index in group:
            names.append(self.course_roster[index].name())
        return names

    def group_list_by_size(self, group_size):
        # Returns a list of the group sizes to be generated,
        #   given a desired group SIZE
        #   If class doesn't divide evenly, it will make groups larger
        class_size = len(self.course_roster)
        list_of_groups = []
        # Integer division, floor
        num_groups = class_size // group_size
        remainder = class_size % group_size
        for i in range(num_groups):
            list_of_groups.append(group_size)
        for i in range(remainder):
            list_of_groups[i] += 1
        return list_of_groups

    def group_list_by_number(self, num_groups):
        """ Returns a list of the group sizes to be generated,
        given a desired NUMBER of groups.
        If class doesn't divide evenly it will make the groups larger
        """
        class_size = len(self.course_roster)
        list_of_groups = []
        # Integer division, floor
        group_size = class_size // num_groups
        remainder = class_size % num_groups
        for i in range(num_groups):
            list_of_groups.append(group_size)
        for i in range(remainder):
            list_of_groups[i] += 1
        return list_of_groups

    def make_groups(self, group_val, group_by):


        # Get matrix of cost
        matrix = self.gen_history_matrix()

        group_sizes = []
        if group_by.startswith("s"):
            group_sizes = self.group_list_by_size(group_val)
        elif group_by.startswith("n"):
            group_sizes = self.group_list_by_number(group_val)

        print(group_sizes)

        # Generate all possible permutations of students
        pair_permutations = itertools.permutations(self.student_indices())

        # Cut those permutations into groups of specified sizes
        grouped_permutations = cast_into_chunks(pair_permutations, group_sizes)

        # Find all groups with the lowest possible score
        best_groups = find_best_groups(grouped_permutations, matrix)

        # Randomly choose one set of groups from the best groups
        return random.choice(best_groups)

class Session:
    def __init__(self, directory):
        # This is the directory in which to look for course files
        self.directory = directory

    def choose_course(self):
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
            choice = "0"

            if choice.startswith("q"):
                quit()
            # If selected index is valid, load the course and return object
            elif int(choice) < len(course_file):
                return Course(self.directory + "/" + course_file[index])


main()
