# - Especifica el conjunto de medidas adoptadas para la creacion de la leyenda geologica, dichas medidas
#   fueron coordinadas con el usuario.
# - La modificacion de la seccion 'VARIABLES' permite la modificacion automatica de las clases establecidas.


# ::::::::::::::::::: VARIABLES :::::::::::::::::::::::::

width_etiqueta = 1000.0   				# 1000.0
heigth_etiqueta = 250.0					# 250.0
space_between_etiqueta = 200.0			# 200.0
margin_top_bootom = 250.0				# 250.0

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::


class distancias_estandar:
	def __init__(self):
		self.col_01_grup = 375
		self.col_01_form_depo = 1500
		self.col_01_marg_form_etiq = 125
		self.col_01_marg_etiq_desc = 125
		self.col_01_desc = 3500
		self.col_01_marg_dere = 125
		self.col_01_suma = self.col_01_marg_etiq_desc + self.col_01_desc + self.col_01_marg_dere
		self.col_02_conj_volc = 450
		self.col_02_desc = 3500
		self.col_02_marg_etiq_desc = 125
		self.col_02_marg_dere = 125
		self.col_02_suma = self.col_02_marg_etiq_desc + self.col_02_desc + self.col_02_marg_dere
		self.col_03_batol = 375
		self.col_03_super_unid = 250
		self.col_03_unid = 250
		self.col_03_pluton = 1265
		self.col_03_marg_plut_etiq = 125
		self.col_03_marg_etiq_desc = 125
		self.col_03_desc = 2985
		self.col_03_marg_dere = 125
		self.col_03_suma = self.col_03_marg_etiq_desc + self.col_03_desc + self.col_03_marg_dere



class ColumAge:
	def __init__(self, xini, yini):
		self.width = 2125.0
		self.heigth = None
		self.colWidth = {
			"eratm": 375.0,
			"sistm": 375.0,
			"serie": 1000.0,
			"edad": 375.0
		}
		self.eratm = {
			"dims": self.colWidth["eratm"],
			"xini": xini,
			"yini": yini,
			"xfin": xini + self.colWidth["eratm"],
			"yfin":  yini
		}
		self.sistm = {
			"dims": self.colWidth["sistm"],
			"xini": self.eratm["xfin"],
			"yini": yini,
			"xfin": self.eratm["xfin"] + self.colWidth["sistm"],
			"yfin":  yini
		}
		self.serie = {
			"dims": self.colWidth["serie"],
			"xini": self.sistm["xfin"],
			"yini": yini,
			"xfin": self.sistm["xfin"] + self.colWidth["serie"],
			"yfin":  yini
		}
		self.edad = {
			"dims": self.colWidth["edad"],
			"xini": self.serie["xfin"],
			"yini": yini,
			"xfin": self.serie["xfin"] + self.colWidth["edad"],
			"yfin":  yini
		}
		self.xini = xini
		self.yini = yini
		self.xfin = self.xini + self.width
		self.yfin = yini


	def yTop(self, heigth):
		y = self.yini + heigth + 550.0
		return y



class ColUnidLito:
	def __init__(self, xini, yini, xfin):
		self.heigth = None
		self.colWidth = {
			"grupo": 375.0,
			"nombr": 1500.0,
			"separ": 125.0,
			"formc": width_etiqueta,
			"descr": 3500.0
		}
		self.grupo = {
			"dims": self.colWidth["grupo"],
			"xini": xini,
			"yini": yini,
			"xfin": xini + self.colWidth["grupo"],
			"yfin": yini,
			"xlbl": (xini*2 + self.colWidth["grupo"])/2
		}
		self.formacion = {
			"dims": self.colWidth["nombr"],
			"xini": self.grupo["xfin"],
			"yini": yini,
			"xfin": self.grupo["xfin"] + self.colWidth["nombr"],
			"yfin": yini,
			"xlbl": self.grupo["xfin"]
		}
		self.separ = {
			"dims": self.colWidth["separ"],
			"xini": self.formacion["xfin"],
			"yini": yini,
			"xfin": self.formacion["xfin"] + self.colWidth["separ"],
			"yfin": yini	
		}
		self.formc = {
			"dims": self.colWidth["formc"],
			"xini": self.separ["xfin"],
			"yini": yini,
			"xfin": self.separ["xfin"] + self.colWidth["formc"],
			"yfin": yini,
		}
		self.descr = {
			"dims": self.colWidth["descr"],
			"xini": self.formc["xfin"] + self.colWidth["separ"],
			"yini": yini,
			"xfin": self.formc["xfin"] + self.colWidth["separ"] + self.colWidth["descr"],
			"yfin": yini
		}
		self.xini = xini
		self.yini = yini
		self.xfin = xfin
		self.yfin = yini


	def yTop(self, heigth):
		y = self.yini + heigth + 550.0
		return y



class ColMorfVolc:
	def __init__(self, xini, yini, xfin):
		self.heigth = None
		self.colWidth = {
			"separ": 450.0,
			"formc": width_etiqueta,
			"descr": 3500.0
		}
		self.separ = {
			"dims": self.colWidth["separ"],
			"xini": xini,
			"yini": yini,
			"xfin": xini + self.colWidth["separ"],
			"yfin": yini	
		}
		self.formc = {
			"dims": self.colWidth["formc"],
			"xini": self.separ["xfin"],
			"yini": yini,
			"xfin": self.separ["xfin"] + self.colWidth["formc"],
			"yfin": yini,
			"simb": {
				"width": self.colWidth["formc"],
				"heigth": heigth_etiqueta,
				"xini": self.separ["xfin"], 
				"yini": yini + self.colWidth["separ"],
				"xfin": self.separ["xfin"] + self.colWidth["formc"],
				"yfin": yini + self.colWidth["separ"]
			}
		}
		self.descr = {
			"dims": self.colWidth["descr"],
			"xini": self.formc["xfin"] + self.colWidth["separ"],
			"yini": yini,
			"xfin": self.formc["xfin"] + self.colWidth["separ"] + self.colWidth["descr"],
			"yfin": yini
		}
		self.xini = xini
		self.yini = yini
		self.xfin = xfin
		self.yfin = yini


	def yTop(self, heigth):
		y = self.yini + heigth + 550.0
		return y




class ColIntrSubv:
	def __init__(self, xini, yini, xfin):
		self.heigth = None
		self.colWidth = {
			"batol": 375.0,
			"grupo": 375.0,
			"separ": 125.0,
			"nombr": 1265,
			"formc": width_etiqueta,
			"descr": 2985.0
		}
		self.batol = {
			"dims": self.colWidth["batol"],
			"xini": xini,
			"yini": yini,
			"xfin": xini + self.colWidth["batol"],
			"yfin": yini
		}
		self.grupo = {
			"dims": self.colWidth["grupo"],
			"xini": self.batol["xfin"],
			"yini": yini,
			"xfin": self.batol["xfin"] + self.colWidth["grupo"],
			"yfin": yini
		}
		self.separ = {
			"dims": self.colWidth["separ"],
			"xini": self.grupo["xfin"],
			"yini": yini,
			"xfin": self.grupo["xfin"] + self.colWidth["separ"],
			"yfin": yini
		}		
		self.nombr = {
			"dims": self.colWidth["nombr"],
			"xini": self.separ["xfin"],
			"yini": yini,
			"xfin": self.separ["xfin"] + self.colWidth["nombr"],
			"yfin": yini,
			"xlbl": self.separ["xfin"]
		}
		self.formc = {
			"dims": self.colWidth["formc"],
			"xini": self.nombr["xfin"] + self.colWidth["separ"],
			"yini": yini,
			"xfin": self.nombr["xfin"] + self.colWidth["separ"] + self.colWidth["formc"],
			"yfin": yini

		}
		self.descr = {
			"dims": self.colWidth["descr"],
			"xini": self.formc["xfin"] + self.colWidth["separ"],
			"yini": yini,
			"xfin": self.formc["xfin"] + self.colWidth["separ"] + self.colWidth["descr"],
			"yfin": yini
		}
		self.xini = xini
		self.yini = yini
		self.xfin = xfin
		self.yfin = yini


	def yTop(self, heigth):
		y = self.yini + heigth + 550.0
		return y



class Annot_unidades_litoestatigraficas:
	def __init__(self):
		self.distancia_descripcion = (width_etiqueta/2) + 125.0 
		self.distancia_grupo = -(width_etiqueta/2) - 1812.5
		self.distancia_formacion_deposito = -(width_etiqueta/2) - 1625.0
		self.distancia_miembro = -(width_etiqueta/2) - 750




class Annot_morfoestructuras_volcanicas:
	def __init__(self):
		self.distancia_descripcion = (width_etiqueta/2) + 125.0
		self.distancia_conjunto_volcanico = -187.5 - (width_etiqueta/2) 	# VALIDAR INFORMACION




class Annot_rocas_intrusivas_subvolcanicas:
	def __init__(self):
		self.distancia_descripcion = (width_etiqueta/2) + 125.0
		self.distancia_batolito = -2572.5
		self.distancia_super_unidad = -2322.5
		self.distancia_unidad = -2072.5
		self.distancia_pluton = -1885.0





# CLASE INDEPENDIENTE SOBRE POSICION DE SIMBOLOS
# MODIFICAR SI ES QUE EXISTE ALGUNA VARIACION EN LAS FUNCIONES ANTERIORES
# *****
class simbol:
	def __init__(self, xini, yini):
		dest = distancias_estandar()
		self.width = width_etiqueta
		self.heigth = heigth_etiqueta
		self.separ = space_between_etiqueta
		self.contemp = {1: self.width + dest.col_01_suma, 2: self.width + dest.col_02_suma, 3: self.width + dest.col_03_suma}
		self.xini = xini
		self.yini = yini + 125
		self.addsp = margin_top_bootom
		self.elev = self.yini + 125
		self.elevSerie = (self.heigth + self.separ)/2


class Coords:
	def __init__(self, state, xini, yini):
		self.state = state
		self.xini = xini		# xini respecto a la columna de edades
		self.yini = yini		# yini respecto a la columna de edades
		self.C1 = {
			"xfin": None,
			"yfin": yini,
			"factor": width_etiqueta + 3750
		}
		self.C2 = {
			"xfin": None,
			"yfin": yini,
			"factor": width_etiqueta + 3750
		}
		self.C3 = {
			"xfin": None,
			"yfin": yini,
			"factor": width_etiqueta + 3360
		}

	#	CONFIGURACION DEL ANCHO DE LA COLUMNA
	@property
	def getCoord(self):
		dest = distancias_estandar()
		acumulator = self.xini
		for k, v in self.state.items():
			if k == 1:
				self.C1["xfin"] = sum([acumulator, dest.col_01_grup, dest.col_01_form_depo, dest.col_01_marg_form_etiq, width_etiqueta*v, dest.col_01_suma*v])
				acumulator = self.C1["xfin"]
			elif k == 2:
				self.C2["xfin"] = sum([acumulator, dest.col_02_conj_volc, width_etiqueta*v, dest.col_02_suma*v])
				acumulator = self.C2["xfin"]
			elif k == 3:
				self.C3["xfin"] = sum([acumulator, dest.col_03_batol, dest.col_03_super_unid, dest.col_03_unid, dest.col_03_pluton, dest.col_03_marg_plut_etiq, width_etiqueta*v, dest.col_03_suma*v])
				acumulator = self.C3["xfin"]
		matriz = {
			1: self.C1,
			2: self.C2,
			3: self.C3
		}
		return matriz