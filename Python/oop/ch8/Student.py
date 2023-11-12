class Student():

    def __init__(self, name, startingGrade=0):
        self.__name = name
        self.grade = startingGrade

    @property
    def grade(self):
        return self.__     grade


    @grade.setter
    def grade(self, newGrade):
        try:
            newGrade = int(newGrade)
        except (TypeError, ValueError) as e:
            raise type(e) ('New grade: ' + str(newGrade) + ', is an invalid type.')

        if (newGrade < 0) or (newGrade > 100):
            raise ValueError('New grade: ' + str(newGrade) + ',must be between 0 and 100.')

        self.__grade = newGrade


if __name__ == '__main__':
    oStudent1 = Student('Shock Lee')
    oStudent2 = Student('Jane Smith')

    print(oStudent1.grade)
    print(oStudent2.grade)
    print()

    oStudent1.grade = 85
    oStudent2.grade = 92

    print(oStudent1.grade)
    print(oStudent2.grade)

