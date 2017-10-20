# -*- CODING: UTF-8 -*-

import arcpy
import json
import qrcode
from configs.model import *
from configs.statics import *


arcpy.env.overwriteOutput = True


class GenerateMap:
	def __init__(self, hoja, sql):
		self.hoja = hoja 
		self.hoja100 = self.hoja[:-1]
		self.sql = sql
		self.sql100 = "{} = '{}'".format(GpoHojas100().codhoja, self.hoja100)		# MODIFICAR EN CASO EL IDENTIFICADOR VARIE
		self.sql50 = "{} = '{}' AND {} = {}".format(GpoHojas50().codhoja, self.hoja100, GpoHojas50().cuadrante, self.hoja[-1])		# MODIFICAR EN CASO EL IDENTIFICADOR VARIE
		self.nombrehoja = [x[0] for x in arcpy.da.SearchCursor(GpoHojas100().path, [GpoHojas100().nombreHoja], self.sql100)][0]
		self.zonaGeografica = [x[0] for x in arcpy.da.SearchCursor(GpoHojas100().path, [GpoHojas100().zonageo], self.sql100)][0]
		self.temp = Template(self.zonaGeografica)					# Statics.py
		self.mxd = arcpy.mapping.MapDocument(self.temp.path)
		self.outqr = self.temp.outqr
		self.dfs = Componentes()				# Statics.py
		self.principal = self.dfs.Principal()	# Statics.py
		self.leyenda = self.dfs.Leyenda()		# Statics.py
		self.caratula = self.dfs.Caratula()		# Statics.py
		self.ubiReg = self.dfs.UbiRegional()	# Statics.py
		self.perfil = self.dfs.Perfil()			# Statics.py
		self.ubiCuad = self.dfs.UbiCuadrante()	# Statics.py
		self.elem = Elements()					# Statics.py
		self.dataciones = self.dfs.Dataciones()			# Statics.py
		self.fosiles = self.dfs.Fosiles()			# Statics.py



	def runQuery(self, objDf, nameLyr=None, lyrExtent=None, scale=None):
		df = arcpy.mapping.ListDataFrames(self.mxd, objDf.name)[0]
		lyrs = {x.name: x for x in arcpy.mapping.ListLayers(self.mxd, nameLyr, df)}
		for k, v in lyrs.items():
			if v.supports("DEFINITIONQUERY"):
				v.definitionQuery = self.sql
		arcpy.RefreshActiveView()
		if lyrExtent:
			self.extentDataFrame(df, lyrs[lyrExtent], scale)
		arcpy.RefreshActiveView()



	def extentDataFrame(self, objDf, objlyr, scale=None):
		objDf.extent = objlyr.getSelectedExtent()
		if scale:
			objDf.scale = scale



	def sheetCurrent(self, objDf, nameLyr):
		df = arcpy.mapping.ListDataFrames(self.mxd, objDf.name)[0]
		lyr = arcpy.mapping.ListLayers(self.mxd, nameLyr, df)[0]
		lyr.definitionQuery = self.sql100


	# CREACION DE CODIGO QR
	@property
	def createQrCode(self):
		pathQr = os.path.join(self.outqr, "{}.png".format(self.hoja))
		img = qrcode.make(self.hoja)
		fileqr = open(pathQr, "wb")
		img.save(fileqr)
		fileqr.close()
		return pathQr



	def addQrToMap(self):
		nameElement = QrCode().element
		element = arcpy.mapping.ListLayoutElements(self.mxd, "PICTURE_ELEMENT", nameElement)[0]
		element.sourceImage = self.createQrCode
		arcpy.RefreshActiveView()




	# DATA FRAME DE UBICACION REGIONAL
	def ubiRegional(self):
		df = arcpy.mapping.ListDataFrames(self.mxd, self.ubiReg.name)[0]
		layer_hoja_actual = arcpy.mapping.ListLayers(self.mxd, self.ubiReg.hojaActual, df)[0]
		layer_hojas_peru = arcpy.mapping.ListLayers(self.mxd, self.ubiReg.hojasPeru, df)[0]
		layer_hoja_actual.definitionQuery = self.sql50
		layer_hojas_peru.definitionQuery = self.sql100
		arcpy.RefreshActiveView()
		df.extent = layer_hojas_peru.getSelectedExtent()
		df.scale = self.ubiReg.scale
		arcpy.RefreshActiveView()



	def ubiCuadrante(self):
		containerSentence = []
		value = self.hoja100[-1]
		row = self.hoja100.split("-")[0]
		filas = [str(int(row) - 1), row, str(int(row) + 1)]
		key = [k for k, v in self.ubiCuad.alpha.items() if v == value][0]
		idxR = self.ubiCuad.alpha[key+1] if self.ubiCuad.alpha.has_key(key+1) else None
		idxL = self.ubiCuad.alpha[key-1] if self.ubiCuad.alpha.has_key(key-1) else None
		columnas = [idxL, value, idxR]
		for x in filas:
			for m in columnas:
				if m:
					sentence = "{} = '{}-{}'".format(GpoHojas100().codhoja, x, m)
					containerSentence.append(sentence)

		df = arcpy.mapping.ListDataFrames(self.mxd, self.ubiCuad.name)[0]
		lyr = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.HojasPeru, df)[0]
		lyr.definitionQuery = " OR ".join(containerSentence)
		df.extent = lyr.getSelectedExtent()
		df.scale = self.ubiCuad.scale

		lyrs50 = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.hojaCuad, df)[0]
		lyrs50.definitionQuery = "{} = '{}'".format(GpoHojas50().codhoja, self.hoja100)

		lyrUpd50 = arcpy.mapping.ListLayers(self.mxd, self.ubiCuad.hojaActual, df)[0]
		lyrUpd50.definitionQuery = self.sql50
		arcpy.RefreshActiveView()


	def updateLabels(self):
		labels = arcpy.mapping.ListLayoutElements(self.mxd, self.elem.datahoja["tipo"], self.elem.datahoja["nombre"])
		for x in labels:
			x.text = u"{} - HOJA {}".format(self.nombrehoja.upper(), self.hoja.upper())
		arcpy.RefreshActiveView()



	# EXPORTAR MAPA EN FORMATO MXD
	def saveMxd(self):
		out = os.path.join(self.temp.outdir, 'CUAD_{}.mxd'.format(self.hoja))
		self.mxd.saveACopy(out)



	def main(self):
		self.runQuery(self.principal, nameLyr=None, lyrExtent=self.principal.extentDf, scale=self.principal.scale)	# PRINCIPAL
		self.runQuery(self.leyenda, nameLyr=None, lyrExtent=self.leyenda.extentDf)									# LEYENDA
		self.runQuery(self.perfil, nameLyr=None, lyrExtent=self.perfil.extentDf, scale=self.perfil.scale)			# PERFIL
		self.runQuery(self.dataciones, nameLyr=None, lyrExtent=self.dataciones.extentDf, scale=None)				# DATACIONES
		self.runQuery(self.fosiles, nameLyr=None, lyrExtent=self.fosiles.extentDf, scale=None)				# DATACIONES
		self.sheetCurrent(self.caratula, self.caratula.hojaActual)
		self.ubiRegional()
		self.ubiCuadrante()
		self.updateLabels()
		self.addQrToMap()
		self.saveMxd()




if __name__ == "__main__":
	poo = GenerateMap("21-i4", "CODHOJA = '21-i4'")
	poo.main()



