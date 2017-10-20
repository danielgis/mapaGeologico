import os


class Statics:
	def __init__(self):
		self.stat = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\statics'


class Conexion:
	def __init__(self):
		self.conn =  os.path.join(Statics().stat, 'MG_DGR_50K.gdb')
		self.bdgeocat = r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\connections\bdgeocat_publ_gis.sde'



class Services:
	def __init__(self):
		self.FEATURE_TO_POLYGON_SERVICE_TOOLBOX = "http://geocatmin.ingemmet.gob.pe:6080/arcgis/rest/services;GEOPROCESO/FeatureToPolygonService"
		self.FEATURE_VERTICES_TO_POINT_SERVICE_TOOLBOX = "http://geocatmin.ingemmet.gob.pe:6080/arcgis/rest/services;GEOPROCESO/FeatureVerticesToPointService"