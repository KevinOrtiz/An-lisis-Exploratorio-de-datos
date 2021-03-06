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

def get_parsed_int(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	list_string = []
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:
			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			raw_string = string.replace(raw_string, '.', '')
			raw_string = string.replace(raw_string, ',', '')
			raw_string = string.replace(raw_string, ';', '')
			raw_string = string.replace(raw_string, ':', '')
			raw_string = string.replace(raw_string, '-', '')
			raw_string = raw_string.split(' ')
			raw_string = raw_string[0]
			return_string = htmlparser.unescape(raw_string)
	return return_string


def get_parsed_string(selector, xpath):
	return_string = ''
	extracted_list = selector.xpath(xpath).extract()
	if len(extracted_list) > 0:
		raw_string = extracted_list[0].strip()
		if raw_string is not None:
			raw_string = raw_string.strip()
			raw_string = unidecode.unidecode(raw_string)
			raw_string = string.replace(raw_string, '\n', '')
			raw_string = string.replace(raw_string, '\"', '')
			return_string = htmlparser.unescape(raw_string)
	return return_string

def get_parsed_date(selector, xpath):
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
			raw_string = string.replace(raw_string, 'Se escribio una opinion ', '')
			aw_string = string.replace(raw_string, 'Reviewed ', '')
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