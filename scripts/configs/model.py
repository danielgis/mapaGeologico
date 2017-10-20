from settings import *


class FGeneral:
	def __init__(self):
		self.codhoja = "CODHOJA"


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::: CAPAS GENERALES :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoGeology:
	def __init__(self, zone):
		self.dsSelect = {17: 2, 18: 3, 19: 4}
		self.codi = "CODI"
		self.codform = "CODFORM"
		self.name = "ETIQUETA"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.nameDs = "DS_0{}_GEOLOGIA_{}S".format(self.dsSelect[zone], zone)
		self.namefc = "GPO_MG_GEOL_{}S".format(zone)
		self.path =  os.path.join(Conexion().conn, self.nameDs, self.namefc)



class GpoQuadrant:
	def __init__(self):
		self.codhoja = "CODHOJA"
		self.cuadr = "CUADR"
		self.zonageo = "ZONAGEO"
		self.nameDs = "DS_01_DATO_GEOG"
		self.path = os.path.join(Conexion().conn, self.nameDs, "GPO_MG_HOJA_50K")



# :::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::  TABLAS :::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class tblegend:
	def __init__(self):
		self.codi = "CODI"
		self.codform = "CODFORM"
		self.name = "ETIQUETA"
		self.grupo = "GRUPO"
		self.formacion = "FORMACION"
		self.deposito = "DEPOSITO"
		self.miembro = "MIEMBRO"
		self.cvolc = "CVOLC"
		self.batol = "BATOLIT"
		self.supuni = "SUP_UNIDAD"
		self.unidad = "UNIDAD"
		self.pluton = "PLUTON"
		self.descrip = "DESCRIP"
		self.serie = "SERIE"
		self.serie_adi = "SERIE_ADI"
		self.tipo = "TIPOFORM"
		self.contform = "CONTFORM"
		self.orden = "ORDEN"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.path = os.path.join(Conexion().conn, "TB_MG_LEYENDA")



class tbage:
	def __init__(self):
		self.id_edad = "ID_EDAD"
		self.id_padre = "ID_PADRE"
		self.nombre = "NOMBRE"
		self.edad_ini = "EDAD_INI"
		self.ei_aprox = "EI_APROX"
		self.edad_fin = "EDAD_INI"
		self.ef_aprox = "EF_APROX"
		self.path = os.path.join(Conexion().conn, 'TB_MG_EDADES')



# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::  FUENTES EXTERNAS  :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoHojas100:
	def __init__(self):
		self.codhoja = "QDR_CODIGO_ALFANUMERICO"
		self.zonageo = "DOM_PROYECCION"
		self.nombreHoja = "QDR_NOMBRE"
		self.nameDs = 'DATA_GIS.DS_PROYECTOS_INGEMMET'
		self.namefc = "DATA_GIS.GPO_HOJ_HOJAS_100"
		self.path = os.path.join(Conexion().bdgeocat, self.nameDs, self.namefc)



class GpoHojas50:
	def __init__(self):
		self.codhoja = "COD_CARTA"
		self.cuadrante = "CUADRANTE"
		self.nameDs = 'DATA_GIS.DS_PROYECTOS_INGEMMET'
		self.namefc = "DATA_GIS.GPO_HOJ_HOJAS_50"
		self.path = os.path.join(Conexion().bdgeocat, self.nameDs, self.namefc)


# :::::::::::::::::::::::::::::::::::::::::::
# ::::::::::  LEYENDA GEOLOGICA :::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::


class GpoLegend:
	def __init__(self):
		self.codi = "CODI"
		self.codform = "CODFORM"
		self.name = "ETIQUETA"
		self.grupo = "GRUPO"
		self.formacion = "FORMACION"
		self.deposito = "DEPOSITO"
		self.miembro = "MIEMBRO"
		self.cvolc = "CVOLC"
		self.batol = "BATOLIT"
		self.supuni = "SUP_UNIDAD"
		self.unidad = "UNIDAD"
		self.pluton = "PLUTON"
		self.descrip = "DESCRIP"
		self.serie = "SERIE"
		self.serie_adi = "SERIE_ADI"
		self.tipo = "TIPOFORM"
		self.contform = "CONTFORM"
		self.orden = "ORDEN"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.nameDs = "DS_07_LEYENDA"
		self.namefc = "GPO_MG_FORM"
		self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)


class GplLegend:
	def __init__(self):
		self.codi = "CODI"
		self.orden = "ORDEN"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.nameDs = "DS_07_LEYENDA"
		self.namefc = "GPL_MG_CELD"
		self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)



class GptLegend:
	def __init__(self):
		self.nombre = "ETIQUETA"
		self.estilo = "ESTILO"
		self.orden = "ORDEN"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.nameDs = "DS_07_LEYENDA"
		self.namefc = "GPT_MG_LABEL"
		self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)




class GlbLegend:
	def __init__(self):
		self.orden = "ORDEN"
		self.hoja = "HOJA"
		self.cuadrante = "CUADRANTE"
		self.codhoja = "CODHOJA"
		self.nameDs = "DS_07_LEYENDA"
		self.namefc = "GAN_MG_LABEL"
		self.path = os.path.join(Conexion().conn, self.nameDs, self.namefc)

