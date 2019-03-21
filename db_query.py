import os

def get_sql(db=r'database_store/city.sql',
    vocab=r'lang_store/english.csv',
    query='Count how many city there are with the name blob?'):

    os.system(r'python -m ln2sql.main -d {} -l {} -j output.json -i "{}"'.format(db, vocab, query))

get_sql()