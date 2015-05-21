'''
Created on May 21, 2015

@author: Likai
'''
import re,urllib, http.cookiejar

def GetHtmlFormVAMK(stuID, password):
    logincookieraw = http.cookiejar.LWPCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(logincookieraw))
    start_path = "https://secure.puv.fi/wille/elogon.asp"
    login_path = "https://secure.puv.fi/wille/elogon.asp?dfUsername?dfPassword?dfUsernameHuoltaja"
    login_data = urllib.parse.urlencode({'dfUsernameHidden' : stuID , 'dfPasswordHidden' : password}).encode()
    left = "https://secure.puv.fi/wille/emainval.asp"
    req_path = "https://secure.puv.fi/wille/eWilleNetLink.asp?Link=https://secure.puv.fi/willenet/HopsSuoritukset.aspx&Hyv=1&Opjakso=&ArvPvm="
    request_data = urllib.parse.urlencode({'rbRajaus' : 'rbSuoritukset' , 'dfOpjakso' : '' , 'dfArviointipvm' : ''}).encode()

    opener.open(start_path)
    opener.open(login_path, login_data)
    opener.open(left)
    return(opener.open(req_path, request_data).read().decode('utf-8'))


def extractCourses(text):
    coursesList = []
    courses = re.findall(r'">\d+,\d+ CR.*?[\dMS]', text) 
    for course in courses:
        course = re.findall('\d+\.\d+|[\dMS]', course.replace(',','.'))
        coursesList.append(course)
    return coursesList

def gpaCalcByCoursesList(coursesList):
    gpa = 0
    normalCredits = 0
    MCredits = 0
    sCredits = 0
    
    CoursesGrades = [0, 0, 0, 0, 0, 0, 0, 0]
    if coursesList != []:
        for course in coursesList:
            if course[1] == 'M':
                CoursesGrades[6] += 1
                MCredits += eval(course[0])
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
    print('*Your GPA: {:4.3f}'.format(gpa))
    print('-----------------Details------------------')
    print('Total credits: ' + str(normalCredits + MCredits + sCredits))
    print('Normal credits: ' + str(normalCredits))
    print('M credits:' + str(MCredits))
    print('S credits:' + str(sCredits))
    print('Grades summary:')    
    for i in range(6):
        print('  Grade {}: {}'.format(i, str(CoursesGrades[i])))
    print('  Grade M: ' + str(CoursesGrades[6]))
    print('  Grade S: ' + str(CoursesGrades[7]))

if __name__ == '__main__':
    while True:
        try:
            print('**************GPA in VAMK*****************')    
            stuID = input('Input your student ID: ')
            password = input('Input your password: ')
            if stuID == '' or password == '':
                raise Exception
            print('Please Wait for a moment..................\n')
            gpaCalcByCoursesList(extractCourses(GetHtmlFormVAMK(stuID, password)))
        except:
            print('Error!')
        finally:
            print('------------------------------------------')
        if(input('Input "q" to continue, or any other key to continue:') == 'q'):
            print('Bye bye! ---- Lebs')
            break
