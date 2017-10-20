from settings import *
import string


class Template:
	def __init__(self, zona):
		self.path = os.path.join(Statics().stat, 'template{}.mxd'.format(zona))
		self.outdir = os.path.join(Statics().stat, 'process')
		self.outqr = os.path.join(Statics().stat, 'qrcode')


class Componentes:
	class Principal:
		def __init__(self):
			self.name = "1 MAPA PRINCIPAL"
			self.gptVolc = "GPT_DS03_Volcanico"
			self.gptPog = "GPT_DS03_Pog"
			self.gpoGeo = "GPT_DS03_Fosil"
			self.gptData = "GPT_DS03_Datacion"
			self.gplVolc = "GPL_DS03_Volcanico"
			self.gplSecc = "GPL_DS03_Seccion"
			self.gplPli = "GPL_DS03_Pliegue"
			self.gplgeom = "GPL_DS03_Geomorfologia"
			self.gplGeo = "GPL_DS03_Geologia"
			self.gplFall = "GPL_DS03_Fallas"
			self.gplDique = "GPL_DS03_Dique"
			self.gpoGeom = "GPO_DS03_Geomorfologia"
			self.gpoAlt = "GPO_DS03_Alteraciones"
			self.gpoMeta = "GPO_DS03_Metamorfico"
			self.gpoGeo = "GPO_DS03_Geologia"

		@property
		def extentDf(self):
			return self.gpoGeo

		@property
		def scale(self):
			sc = 50000
			return sc


	class Leyenda:
		def __init__(self):
			self.name = "2 LEYENDA"
			self.glb = "GAN_DS07_Etiquetas"
			self.gpl = "GPL_DS07_Celdas"
			self.gpo = "GPO_DS07_Formaciones"

		@property
		def extentDf(self):
			return self.gpl


	class Fosiles:
		def __init__(self):
			self.name = "3 FOSILES"
			self.glb = "GAN_DS06_Anotaciones"
			self.gplFosil = "GPL_DS06_Fosil"

		@property
		def extentDf(self):
			return self.gplFosil


	class Dataciones:
		def __init__(self):
			self.name = "4 DATACIONES"
			self.glb = "GAN_DS05_Anotaciones"
			self.gplData = "GPL_DS05_Datacion"

		@property
		def extentDf(self):
			return self.gplData


	class Simbolos:
		def __init__(self):
			self.name = "5 SIMBOLOS"



	class UbiRegional:
		def __init__(self):
			self.name = "6 MAPA DE UBICACION REGIONAL"
			self.hojaActual = "GPO_HojaActual_50k"
			self.hojasPeru = "GPO_HojasPeru_100k"


		@property
		def scale(self):
			sc = 2500000
			return sc


	class UbiCuadrante:
		def __init__(self):
			self.name = "7 UBICACION DE CUADRANTE"
			self.hojaCuad = "GPO_HojasCuad_50k"
			self.hojaActual = "GPO_HojaActual_50k"
			self.HojasPeru = "GPO_HojasPeru_100k"
			alphaTmp = ",".join(string.ascii_lowercase).split(",")
			alphaTmp.insert(14, '\xd1')
			self.alpha = {k: x.lower() for k, x in enumerate(alphaTmp)}

		@property
		def scale(self):
			sc = 2500000
			return sc


	class Membrete:
		def __init__(self):
			self.name = "8 MEMBRETE"


	class Caratula:
		def __init__(self):
			self.name = "9 CARATULA"
			self.hojasPeru = "GPO_HojasPeru_100k"
			self.hojaActual = "GPO_HojaActual_100k"
			self.limites = "GPL_DS01_Limites"
			self.lago = "GPO_DS01_LagoTiticaca"


	class DecMagnetica:
		def __init__(self):
			self.name = "10 DECLINACION MAGNETICA"


	class Perfil:
		def __init__(self):
			self.name = "11 PERFIL Y SECCION GEOLOGICA"
			self.glb = "GAN_DS08_Anotaciones"
			self.gpl = "GPL_DS08_Celdas"
			self.gpo = "GPO_DS08_Formaciones"

		@property
		def extentDf(self):
			return self.gpl

		@property
		def scale(self):
			sc = 50000
			return sc



class QrCode:
	def __init__(self):
		self.x = 84
		self.y = 7
		self.heigth = 4
		self.width = 4
		self.element = "QRCODE"



class Scale:
	def __init__(self):
		self.mp = 50000
		self.lg = 50000



class Elements:
	def __init__(self):
		self.datahoja = {
			"nombre": "DATAHOJA",
			"tipo": "TEXT_ELEMENT"
		}



class jsonfiles:
	def __init__(self):
		self.gpl = os.path.join(Statics().stat, 'json\leyendaLinea.json')
		self.gpo = os.path.join(Statics().stat, 'json\leyendaPoligono.json')
		self.gpt = os.path.join(Statics().stat, 'json\leyendaPunto.json')



class Annotation:
	def __init__(self):
		self.head_age_label = {
			1: "ERATEMA",
			2: "SISTEMA",
			3: "SERIE",
			4: "EDAD (MA)"
		}
		self.head_column_label = {
			1: u"UNIDADES LITOESTATIGRAFICAS",
			2: u"MORFOESTRUCTURAS VOCANICAS",
			3: u"ROCAS INTRUSIVAS Y SUBVOLCANICAS"
		}
		self.headClass = {
			"ages": 1,
			"colum": 2
		}
		self.laterClass = {
			"eratema": 3,
			"sistema": 4,
			"serie": 5,
			"edad": 6
		}
		self.annotationClass = {
			"descripcion": 7,
			"grupo": 8,
			"formacion_deposito": 9,
			"miembro": 10,
			"conjunto_volcanico": 11,
			"batolito": 12,
			"super_unidad": 13,
			"unidad": 14,
			"pluton": 15
		}
