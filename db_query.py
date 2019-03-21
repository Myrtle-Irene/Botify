import os

def get_sql(db=r'database\city.sql',
    vocab=r'ln2sql\lang\english.csv',
    query='how many city there are in which the employee name is similar to aman ?'):

    os.system(r'python ln2sql\ln2sql.py -d {} -l {} -j output.json -i \
         "{}"'.format(db, vocab, query))

get_sql()