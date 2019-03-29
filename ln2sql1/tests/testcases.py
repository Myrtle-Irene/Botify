import StringIO
import sys,re
import os
import difflib

sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from ln2sql import main as ln2sql_main

reload(sys)
sys.setdefaultencoding("utf-8")

BASE_PATH = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
DATABASE_PATH = os.path.join(BASE_PATH, 'database/')
LANG_PATH = os.path.join(BASE_PATH, 'lang/')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestClass():

    success = 0
    failure = 0

    def __init__(self):
        self.success = 0
        self.failure = 0

    def _cleanOutput(self,s):
        s = s.split("SELECT")[1]  # remove table schema
        s = re.sub("\\033.*?m", "", s)  # remove color codes
        s = s.replace('\n', ' ')  # remove '\n'
        s = s.split(';')[0]  # remove spaces after ;
        s = "SELECT" + s + ';'  # put back lost SELECT and ';'
        return s


    def _printTest(self,status,input,output,outputRetrieved):
        if status == "PASS" :
            print Bcolors.OKBLUE + "---- PASSED ----" + Bcolors.ENDC + "\n"
            print "-> " + input + "\n"
            print Bcolors.OKBLUE + "=> " + outputRetrieved + Bcolors.ENDC + "\n"
            print "----------------------------------------------------------\n"
            print
        if status == "FAIL" :
            differenceList = [li for li in difflib.ndiff(outputRetrieved.split(),output.split()) if li[0] != ' ']
            print Bcolors.BOLD + Bcolors.FAIL + "---- FAILED ----" + Bcolors.ENDC + "\n"
            print "-> " + input + "\n"
            print Bcolors.WARNING + "GETTING  : " + outputRetrieved + Bcolors.ENDC + "\n"
            print Bcolors.WARNING + "EXPECTED : " + output + Bcolors.ENDC + "\n"
            print Bcolors.BOLD + Bcolors.FAIL + str(differenceList) + Bcolors.ENDC + "\n"
            print "-------------------------------------------------------- \n"

        return


    def runTests(self):

        allTests = [
            {
                'input': 'List me the info of city table',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': 'SELECT * FROM city;'
            },
            {
                'input': 'What is the number of the city in this database?',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': 'SELECT COUNT(*) FROM city;'
            },
            {
                'input': 'Count how many city there are where the name is Matthew ?',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.name = 'matthew';"
            },
            {
                'input': 'Count how many city there are where the score is greater than 2 ?',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score > '2';"
            },
            {
                'input': 'Tell me all id from city',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': 'SELECT city.id FROM city;'
            },
            {
                'input': 'What are the name of emp',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': 'SELECT emp.name FROM emp;'
            },
            {
                'input': 'List all name and score of all emp',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': 'SELECT emp.name, emp.score FROM emp;'
            },
            {
                'input': 'What is the emp with the name is rupinder ?',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT * FROM emp WHERE emp.name = 'rupinder';"
            },
            {
                'input': "Show data for city where cityName is 'Pune Agra'",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT * FROM city WHERE city.cityName = 'pune agra';"
            },
            {
                'input': "Show data for city where cityName is not Pune and id like 1",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT * FROM city WHERE city.cityName != 'pune' AND city.id LIKE '%1%';"
            },
            {
                'input': 'What is the cityName and the score of the emp whose name is matthew',
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'matthew';"
            },
            {
                'input': "What is the cityName and the score of the emp whose name is rupinder",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'rupinder';"
            },
            {
                'input': "count distinctly how many city there are ordered by name in descending and ordered by score?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "Count distinctly how many different name of city there are ordered by name in descending and ordered by score?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(DISTINCT emp.name) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "What are the distinct name of city with a score equals to 9?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT DISTINCT emp.name FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score = '9';"
            },
            {
                'input': "count how many city there are ordered by name",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name ASC;"
            },
            {
                'input': "count how many city there are ordered by name in descending order and ordered by score in ascending order",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "count how many city there are ordered by name in descending order and ordered by score?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
            },
            {
                'input': "What is the name and cityId of the emp whose name is Mark and whose cityId is greater than 14 grouped by cityId?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT emp.name, emp.cityId FROM emp WHERE emp.name = 'mark' AND emp.cityId > '14' GROUP BY emp.cityId;"
            },
            {
                'input': "Show data for city where cityName is not vibgyor and id like 1",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT * FROM city WHERE city.cityName != 'vibgyor' AND city.id LIKE '%1%';"
            },
            {
                'input': "Show data for city where cityName is not 'vibgyor or' and id like 1",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT * FROM city WHERE city.cityName != 'vibgyor or' AND city.id LIKE '%1%';"
            },
            {
                'input': "how many name there are in emp in which the cityId is more than 3 ?",
                'database': DATABASE_PATH + 'city.sql',
                'language': LANG_PATH + 'english.csv',
                'output': "SELECT COUNT(emp.name) FROM emp WHERE emp.cityId > '3';"
            }

        ]

        for test in allTests:
            capturedOutput = StringIO.StringIO()
            sys.stdout = capturedOutput
            ln2sql_main(['-d', test['database'], '-l', test['language'], '-i', test['input']])
            sys.stdout = sys.__stdout__
            outputRetrieved = self._cleanOutput(capturedOutput.getvalue())

            if outputRetrieved == test['output'] :
                status = "PASS"
                self.success += 1
                self._printTest(status,test['input'],test['output'],outputRetrieved)
            else :
                status = "FAIL"
                self.failure += 1
                self._printTest(status,test['input'],test['output'],outputRetrieved)



if __name__ == '__main__':
    print "== == == == == == == == == == == == == == == == == == == == == == == \n"
    obj = TestClass()
    obj.runTests()
    print Bcolors.WARNING + " +--------------------------" + Bcolors.ENDC 	
    print Bcolors.WARNING + " |  " + Bcolors.OKBLUE + "Testcases Passed : " + str(obj.success) + Bcolors.ENDC
    print Bcolors.WARNING + " |  " + Bcolors.BOLD + Bcolors.FAIL + "Testcases Failed : " + str(obj.failure) + Bcolors.ENDC 
    print Bcolors.WARNING + " +--------------------------\n" + Bcolors.ENDC
    	

