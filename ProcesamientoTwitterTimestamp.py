import pandas as pd
import dateutil.parser as dateparser
import datetime
import time


def procesamiento_Timestamp():
	datos = pd.read_csv('tweets_depurated_noText.csv')
	#datos['timestamstamp_ms'] = datos['timestamstamp_ms'].astype(int)
	#print datos['timestamstamp_ms']
	datos['weekday'] = datos['timestamstamp_ms'].apply(valorWeekDay)
	datos['horas'] = datos['timestamstamp_ms'].apply(valorHoras)
	datos['day'] = datos['timestamstamp_ms'].apply(valorDay)
	datos['Sol_Weekend'] = datos['timestamstamp_ms'].apply(valorDayWeekend)
	#print  datos['timestamstamp_ms'].apply(lambda x:valorDayWeekend)
	datos['Fecha'] = datos['timestamstamp_ms'].apply(Fecha)
	datos['diaSemana'] = datos['timestamstamp_ms'].apply(DiaSemana)
	datos['HoraTweet'] = datos['timestamstamp_ms'].apply(ZonaHoraria)

	datos.to_csv('ArchivoCategorizadoTimestamp.csv')

def ZonaHoraria(x):
	y = datetime.datetime.fromtimestamp(x/1000.0)
	return y.strftime("%H:%M:%S")

def DiaSemana(x):
	y = datetime.datetime.fromtimestamp(x/1000.0)
	return y.strftime('%A')
	
def Fecha(x):
	 y = datetime.datetime.fromtimestamp(x/1000.0)
	 return y.date()


def valorWeekDay(x):
	weekDay = datetime.datetime.fromtimestamp(x/1000.0)
	return weekDay.weekday()


def valorHoras(x):
	hours = datetime.datetime.fromtimestamp(x/1000.0)
	return hours.hour


def valorDay(x):
	hours = valorHoras(x)
	if (hours >= 7 and hours <= 18):
		return 1
	else :
		return 0



def valorDayWeekend(x):
	hours = valorHoras(x)
	weekday = valorWeekDay(x)
	print '#####################'
	print 'hours'
	print hours
	print 'weekday'
	print weekday
	print '######################'
	esDia = 1 if hours <=18 and hours >= 7 else 0
	esWeekend = 1 if weekday == 4 or weekday == 5 or weekday == 6 else 0 
	print '#####################'
	print 'esDia'
	print esDia
	print 'esWeekend'
	print esWeekend

	if esDia and esWeekend:
		return 1
	else:
		return 0


if __name__ == '__main__':
	procesamiento_Timestamp()








