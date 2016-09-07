#! /usr/bin/python
import sys
import glob
import numpy
import ast
from numpy import matrix
from numpy import linalg
from matplotlib import pyplot

######################################
#
# Document input

def create_matriz_TFIDF(category,type_word,dominnio):
	# Structures holding documents and terms
	document_list = []	# will contain a list of documents, stored as dictionaries.
						# index in this list is used as ID of document
	document_ids = {}	# reverse search: from document name to corresponding ID
	token_list = []		# List of token strings; index is token's ID
	token_ids = {}		# Reverse dictionary: from token string to ID
	ids_word = {}	
	lista_documento = []
	# Crear el archivo CSV
	csv_file = create_file(category,type_word,dominnio)
	cabecera_csv = 'documentos'

	# Repeat for every document in processed_pages
	for filename in glob.glob(category+'/'+type_word+'/'+dominnio+'/*'):
		# Read the document as list of blank-separated tokens
		tokens = create_tokens(filename)

		# Get the document name as last part of path
		article_name = create_list_document(filename)
		# Crea lista de nombre de archivos
		lista_documento.append(article_name)
		
		# Document's ID is the length of the current document list
		doc_id = len(document_list)
		# Insert ID in inverse list
		document_ids[article_name] = doc_id
		# Crear lista de tokens
		token_list = create_list_tokens(tokens, token_ids, token_list)
		# Transform the document's token list into the corresponding ID list
		tids = [token_ids[t] for t in tokens]
		document_list.append({
			'name': article_name,
			'tokens': tids,
			'set': set(tids)
		})

	# At the end of the loop, we have the total number of documents and tokens
	number_of_documents = len(document_list)
	number_of_tokens = len(token_list)
	sys.stderr.write ('%d documents, %d tokens\n' % (number_of_documents, number_of_tokens))

	##############################################
	#
	# Building the TF-IDF matrix
	sys.stderr.write ('Building the TF matrix and counting term occurrencies\n')
	# For each term, count how many documents contain it (to compute IDF)
	token_count = [0] * number_of_tokens
	#print "token_count:",len(token_count)
	# Alloc the |T|x|D| TFIDF matrix. No need to initialize its entries
	TFIDF = numpy.empty((number_of_tokens,number_of_documents), dtype=float)

	# Creare la matriz TFIDF
	TFIDF = create_TFIDT(document_list,number_of_tokens,token_count,TFIDF)
	# Crear cabecera del CSV
	cabecera_csv = create_cabecera_csv(token_list,cabecera_csv)
	# Escribir la cabecera en el archivo CSV
	csv_file.write(cabecera_csv)
	# Hallar la tranpuesta de la matrix TFIDF
	TFIDF_Transpose = TFIDF.T 
	# Escribir en el archivo CSV
	csv_file = write_csv_TFIDF(TFIDF_Transpose,lista_documento,csv_file)
	# Cerrar archivo CSV
	csv_file.close()


def write_csv_TFIDF(TFIDF_Transpose,lista_documento,csv_file):
	for id_word,lista_coef in enumerate(TFIDF_Transpose):
		line = lista_documento[id_word]
		for coef in lista_coef:
			line = str(line) +','+str(coef)
		line = line+'\n'
		csv_file.write(line)
	return csv_file


def create_cabecera_csv(token_list, cabecera_csv):
	for word in token_list:
		cabecera_csv = cabecera_csv +','+ word
	cabecera_csv = cabecera_csv + '\n'
	return cabecera_csv


def create_TFIDT(document_list,number_of_tokens,token_count,TFIDF):
	# Scan the document list
	for i,doc in enumerate(document_list):
		# For each term, count the number of occurrences within the document
		# Initialize with zeros
		n_dt = [0] * number_of_tokens
		# For all token IDs in document
		for tid in doc['tokens']:
			# if first occurrence, increase global count for IDF
			if n_dt[tid] == 0:
				token_count[tid] += 1
			# increase local count
			n_dt[tid] += 1
		# Normalize local count by document length obtaining TF vector;
		# store it as the i-th column of the TFIDF matrix.
		TFIDF[:,i] = numpy.array(n_dt, dtype=float) / len(doc['tokens'])
	return TFIDF


def create_file(category,type_word,dominnio):
	name_hotel = str(category+'/TF_IDF_POI/'+dominnio+'/'+type_word+'_'+category+'_TFIDF_POI_'+dominnio+'.csv')
	return  open(''+name_hotel,'w')


def create_tokens(filename):
	# Read the document as list of blank-separated tokens
	f = open (filename, 'r')
	tokens = f.read().split('\n')
	tokens = ast.literal_eval(tokens[1])
	# Cerrar la instancia del archivo
	f.close()
	return tokens


def create_list_document(filename):
	# Get the document name as last part of path
	article_name = filename[filename.rfind('/')+1:]
	sys.stderr.write ('Processing document %s...\n' % article_name)
	return article_name


def create_list_tokens(tokens,token_ids,token_list):
	# Populate token structure for all tokens in document
	for t in tokens:
		# Only if token hasn't been seen yet
		if t not in token_ids:
			# Token's ID is token list length
			token_ids[t] = len(token_list)
			# Append token to list
			token_list.append(t)
	return token_list


def create_document_list(article_name,tids):
	# Store the document as both its token ID list and the corresponding set
	# Also remember the document's name
	document_list.append({
		'name': article_name,
		'tokens': tids,
		'set': set(tids)
	})
	return document_list


if __name__ == '__main__':

	print "Hoteles-Adjectives"
	#create_matriz_TFIDF('Hoteles','Adjectives','co')
	#create_matriz_TFIDF('Hoteles','Adjectives','com')
	print "Hoteles-Nouns"
	#create_matriz_TFIDF('Hoteles','Nouns','co')
	#create_matriz_TFIDF('Hoteles','Nouns','com')

	print "Actividades-Adjectives"
	create_matriz_TFIDF('Actividades','Adjectives','co')
	create_matriz_TFIDF('Actividades','Adjectives','com')
	print "Actividades-Nouns"
	create_matriz_TFIDF('Actividades','Nouns','co')
	create_matriz_TFIDF('Actividades','Nouns','com')
