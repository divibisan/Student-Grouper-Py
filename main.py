import itertools
import os


def main():
    # Create new session
    session = Session("classfiles")

    # Select course
    course = session.choose_course()

    print(course.filename)
    course.print_students()

    # Get student pairs and history matrix
    pairs = course.gen_pairs()
    matrix = course.gen_history_matrix()

    # Print matrix
    for row in matrix:
        print(row)

    # Show all pairs and number of times pair has been together
    find_groups(pairs, matrix)

    course.save()


def find_groups(pairs, matrix):
    # Prints sets of groups with the cost of each group
    # Does not ignore repeated groups (0,1 + 2,3 vs 2,3 + 0,1)
    for a, b in pairs:
        print(a, b, matrix[a][b])
        new_pairs = [(c, d) for c, d in pairs if c != a and c != b and d != a and d != b]
        find_groups(new_pairs, matrix)
        print("---")


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
