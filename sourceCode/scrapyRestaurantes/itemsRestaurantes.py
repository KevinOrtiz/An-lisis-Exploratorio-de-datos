import scrapy as sc
import unidecode
import string
from scrapy.loader.processors import TakeFirst, MapCompose, Join



class itemsRestaurantes(sc.Item):
        tituloLugar = sc.Field(
        			input_processor = MapCompose(unicode.strip,
        				lambda x:unidecode.unidecode(x),
        				lambda y:string.replace(y,'\n','')),
        			
        			out_processor = Join(),
        )
        tituloComentario = sc.Field(	
        			input_processor = MapCompose(unicode.strip,
        				lambda x:unidecode.unidecode(x),
        				lambda y:string.replace(y,'\n','')),
        			out_processor = Join(),
        )
        latitud = sc.Field()
        longitud = sc.Field()
        comentarios = sc.Field(	
        			input_processor = MapCompose(unicode.strip,
        				lambda x:unidecode.unidecode(x),
        				lambda y:string.replace(y,'\n','')),
        			out_processor = Join(),

        )
        estrellas = sc.Field(
        			input_processor = MapCompose(unicode.strip,
        			lambda x:x.replace('de 5 estrellas','')),
        			out_processor = Join(),

        )
