import itertools
import os
import random


def main():
    # Create new session
    session = Session("classfiles")

    # Select course
    course = session.choose_course()

    matrix = course.gen_history_matrix()

    print(course.filename)
    course.print_students()

    possible_groups = {}

    pair_permutations = itertools.permutations(course.student_indices())
    for permutation in pair_permutations:
        pairs = chunks(permutation, 2)
        group_set = []
        score = 0
        for pair in pairs:
            a, b = pair
            score += matrix[a][b]
            if a < b:
                pair = (a, b)
            else:
                pair = (b, a)
            group_set.append(pair)

        possible_groups[flatten(group_set)] = score

    # Find minimum cost for group
    min_cost = min(possible_groups.values())

    # Select all possible permutations of groups with minimum cost
    best_options = [k for k, v in possible_groups.items() if v == min_cost]

    # Choose a random possible set of groups from the best options
    chosen_groups = random.choice(best_options)
    print(chosen_groups)

    # Convert from string to list of tuples of ints
    final_groups = []
    for p in chosen_groups.split("."):
        try:
            a, b = p.split(",")
        except ValueError:
            break
        pair = (int(a),int(b))
        final_groups.append(pair)
    print(final_groups)

    # Convert from student indices to names
    for group in final_groups:
        a, b = group
        print(course.course_roster[a].name()
              + " and "
              + course.course_roster[b].name())


def flatten(list):
    flat_list = ""
    for tup in list:
        a, b = tup
        flat_list += str(a) + ","
        flat_list += str(b) + "."
    return flat_list


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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
            choice = input()

            if choice.startswith("q"):
                quit()
            # If selected index is valid, load the course and return object
            elif int(choice) < len(course_file):
                return Course(self.directory + "/" + course_file[index])


main()
