'''
Created on May 21, 2015

@author: Likai
'''
import re

FILE_PATH = 'D:\\Desktop\\text.txt'

def readFromFile(fielPath):
    f = open(fielPath, 'r')
    text = f.read()
    f.close()
    return text


def extractCourses(text):
    coursesList = []
    courses = re.findall('<td>\d+,\d+ CR.*?[\dMS]</td>', text)
    courses = re.findall(r'">\d+,\d+ CR.*?[\dMS]', text)
    for course in courses:
#       course = course.replace(' CR</td><td>&nbsp;</td><td>&nbsp;</td><td>', ';').replace('<td>', '').replace('</td>', '').replace(',', '.').split(';')
        course = re.findall('\d+\.\d+|[\dMS]', course.replace(',','.'))
        coursesList.append(course)
    return coursesList

def gpaCalcByCoursesList(coursesList):
    gpa = 0
    normalCredits = 0
    transferredCredits = 0
    sCredits = 0
    
    CoursesGrades = [0, 0, 0, 0, 0, 0, 0, 0]
    if coursesList != []:
        for course in coursesList:
            if course[1] == 'M':
                CoursesGrades[6] += 1
                transferredCredits += eval(course[0])
            elif course[1] == 'S':
                CoursesGrades[7] += 1
                sCredits += eval(course[0])
            elif eval(course[1]) == 0:
                CoursesGrades[0] += 1
            else:
                gpa += eval(course[0]) * eval(course[1])
                normalCredits += eval(course[0])
                CoursesGrades[eval(course[1])] += 1
        gpa /= normalCredits
    print('Your GPA: {:4.3f}'.format(gpa))
    print('----------------Details-----------------')
    print('Total credits: ' + str(normalCredits + transferredCredits + sCredits))
    print('Normal credits: ' + str(normalCredits))
    print('Transferred credits:' + str(transferredCredits))
    print('S credits:' + str(sCredits))
    print('Grades summary:')    
    for i in range(6):
        print('  Grade {}: {}'.format(i, str(CoursesGrades[i])))
    print('  Grade M: ' + str(CoursesGrades[6]))
    print('  Grade S: ' + str(CoursesGrades[7]))

if __name__ == '__main__':    
    gpaCalcByCoursesList(extractCourses(readFromFile(FILE_PATH)))
