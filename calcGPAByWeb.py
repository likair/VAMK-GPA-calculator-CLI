#!/usr/bin/python3
'''
Created on May 21, 2015

@author: Likai
'''
import re, urllib, http.cookiejar, getpass, platform, functools, sys

def GetHtmlFormVAMK(stuID, password):
    loginCookie = http.cookiejar.LWPCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(loginCookie))
    startUrl = "https://secure.puv.fi/wille/elogon.asp"
    loginUrl = "https://secure.puv.fi/wille/elogon.asp?dfUsername?dfPassword?dfUsernameHuoltaja"
    loginData = urllib.parse.urlencode({'dfUsernameHidden' : stuID , 'dfPasswordHidden' : password}).encode()
    leftFrameUrl = "https://secure.puv.fi/wille/emainval.asp"
    requestUrl = "https://secure.puv.fi/wille/eWilleNetLink.asp?Link=https://secure.puv.fi/willenet/HopsSuoritukset.aspx&Hyv=1&Opjakso=&ArvPvm="
    requestData = urllib.parse.urlencode({'rbRajaus' : 'rbSuoritukset' , 'dfOpjakso' : '' , 'dfArviointipvm' : ''}).encode()
    opener.open(startUrl)
    print('.....', end='', flush=True)
    opener.open(loginUrl, loginData)
    print('......', end='', flush=True)
    opener.open(leftFrameUrl)
    print('......', file=sys.stdout, flush=True)
    return(opener.open(requestUrl, requestData).read().decode('utf-8'))


def extractCourses(text):
    coursesList = []
    courses = re.findall(r'["d]>\d+,\d+ [CO].*?>[\dMS]<', text)
    for course in courses:
        course = re.findall(r'\d+\.\d+|&nbsp;|[\dMS]', course.replace(',', '.'))
        course.pop(1)
        course.pop(1)
        coursesList.append(course)
    return coursesList

def generateReport(coursesList):
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
        totalCourses = functools.reduce(lambda x, y: x + y, CoursesGrades)
        print('------------------------------------------')
        print('             *REPORT CARD*\n')
        if 0 <= gpa < 0.5:
            print('- Oh, what happened?')
        if 0.5 <= gpa < 1.5 :
            print('- Give me a reason, how it is possible?')
        elif 1.5 <= gpa < 2.5:
            print('- Hey, poor guy, you shouldn\'t be like this!')
        elif 2.5 <= gpa < 3.5:
            print('- Come on, You are very promising, but should study harder. ')
        elif 3.5 <= gpa < 4.5:
            print('- OK, you own an enviable GPA!')
        elif 4.5 <= gpa < 5:
            print('- Gorgeous! I must admit that you are a genius!')
        print('* Your GPA: {:4.3f}'.format(gpa))
        print('-----------------DETAILS------------------')
        print('* Total credits: {:5}'.format(normalCredits + MCredits + sCredits))
        print('* Normal credits:{:5}'.format(normalCredits))
        print('* M credits:     {:5}'.format(MCredits))
        print('* S credits:     {:5}'.format(sCredits))
        print('* Grades summary:')
        for i in range(6):
            print('  - Grade {}: {:4} ({:6.2%})'.format(i, CoursesGrades[i], CoursesGrades[i] / totalCourses))
        print('  - Grade {}: {:4} ({:6.2%})'.format('M', CoursesGrades[6], CoursesGrades[6] / totalCourses))
        print('  - Grade {}: {:4} ({:6.2%})'.format('S', CoursesGrades[7], CoursesGrades[7] / totalCourses))
    else:
        print('No course!')

if __name__ == '__main__':
    while True:
        try:
            print('**************GPA in VAMK*****************')
            print('* AUTHENTICATION')
            stuID = input('  Student ID: ').strip()
            password = getpass.getpass('  Password: ').strip()
            if stuID == '' or password == '':
                raise Exception
            print('Please Wait for a moment.', end='', file=sys.stdout, flush=True)
            generateReport(extractCourses(GetHtmlFormVAMK(stuID, password)))
        except:
            print('\nError! Please confirm your student ID/password and if there is network connection.')
        finally:
            print('------------------------------------------')
        if(platform.system() == 'Linux' or input('Input "q" to quit, or any other key to continue:') == 'q'):
            print('Bye bye! ---- Lebs')
            break
