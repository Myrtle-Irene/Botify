import os

def get_sql(db=r'E:\Торренты\Coding\11\1111\ln2sql\ln2sql\database_store\city.sql',
	vocab=r'E:\Торренты\Coding\11\1111\ln2sql\ln2sql\lang_store/english.csv',
	query='Count how many city there are with the name blob?'):

	os.system('python -m ln2sql.main -d {} -l {} -j output.json -i \
		"{}"'.format(db, vocab, query))