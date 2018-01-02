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
            self.index = len(course.course_roster)
            # If no last name provided, use intex as
            try:
                self.lastName = x[1]
            except IndexError:
                self.lastName = str(self.index)
            self.history = [int(num) for num in "0" * len(course.course_roster)]

    def name(self):
        """Return full name by merging first and last"""
        return self.firstName + " " + self.lastName

    def save_record(self):
        """Return comma separated record ready to be written to save file"""
        history_joined = ",".join([str(x) for x in self.history])
        return ",".join([str(self.index), self.firstName,
                         self.lastName, history_joined])
