__author__ = 'cesar17'
import HTMLParser
import unicodedata
import unidecode
import string

htmlparser = HTMLParser.HTMLParser()

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def clean_parsed_string(string):
	if len(string) > 0:
		ascii_string = string
		if is_ascii(ascii_string) == False:
			ascii_string = unicodedata.normalize('NFKD', ascii_string).encode('ascii', 'ignore')
		return str(ascii_string)
	else:
		return None

def get_parsed_string(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	#print "string: ", extracted_list
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:

			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, ',', ' ')
			return_string = htmlparser.unescape(raw_string)
	return return_string

def get_parsed_rating(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:

			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, ',', ' ')
			raw_string = string.replace(raw_string, ' de 5 estrellas', '')
			raw_string = string.replace(raw_string, ' of 5 starts', '')
			raw_string = string.replace(raw_string, 'Escribio una opinion el ', '')
			raw_string = string.replace(raw_string, 'Reviewed', '')
			return_string = htmlparser.unescape(raw_string)
	return return_string

def get_parsed_helpful(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:

			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, ',', ' ')
			raw_string = string.replace(raw_string, ' votos utiles', '')
			raw_string = string.replace(raw_string, ' helpful votes', '')
			return_string = htmlparser.unescape(raw_string)
	return return_string

def get_parsed_date(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:

			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, ',', ' ')

			raw_string = string.replace(raw_string, 'Enero', 'Jan')
			raw_string = string.replace(raw_string, 'Febrero', 'Feb')
			raw_string = string.replace(raw_string, 'Marzo', 'Mar')
			raw_string = string.replace(raw_string, 'Abril', 'Apr')
			raw_string = string.replace(raw_string, 'Mayo', 'May')
			raw_string = string.replace(raw_string, 'Junio', 'Jun')
			raw_string = string.replace(raw_string, 'Julio', 'Jul')
			raw_string = string.replace(raw_string, 'Agosto', 'Aug')
			raw_string = string.replace(raw_string, 'Septiembre', 'Sep')
			raw_string = string.replace(raw_string, 'Octubre', 'Oct')
			raw_string = string.replace(raw_string, 'Noviembre', 'Nov')
			raw_string = string.replace(raw_string, 'Diciembre', 'Dec')

			return_string = htmlparser.unescape(raw_string)
	return return_string

def get_parsed_opinions(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:

			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, ',', ' ')
			raw_string = string.replace(raw_string, ' opiniones sobre hoteles', '')
			raw_string = string.replace(raw_string, ' hotel reviews', '')
			return_string = htmlparser.unescape(raw_string)
	return return_string
	
def get_parsed_string_multiple(selector, xpath):
	return_string = ''
	extracted_review = selector.xpath(xpath).extract()

	list_reviews = []
	for review in extracted_review:
		if review:
			raw_string = review.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')

			list_reviews.append(raw_string)

	return list_reviews