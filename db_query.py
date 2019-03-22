import os
def get_sql(db=r'ln2sql/database/city.sql', vocab=r'ln2sql/lang/english.csv', 
	query=r'how many city there are in which the employee name is similar to aman ?'):
	os.system(r'''C:\Python27\python.exe ln2sql/ln2sql.py -d {} -l {} -j output.json -i "{}"'''.format(db,vocab, query))

get_sql()