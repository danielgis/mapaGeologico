# -*- CODING: UTF-8 -*-

import sys
sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')

from legendProcess import *
from annotationProcess import *
import pythonaddins


class MainLegend:
	def __init__(self):
		self.column = arcpy.GetParameterAsText(0)
		self.row = arcpy.GetParameterAsText(1)
		self.quadrant = arcpy.GetParameterAsText(2)
		self.codhoja = FGeneral().codhoja
		self.code = "{}-{}{}".format(self.column, self.row.lower(), self.quadrant)
		self.sql = "{} = '{}'".format(self.codhoja, self.code)



	def add_all_layers(self):
		mxd = arcpy.mapping.MapDocument("CURRENT")
		df = arcpy.mapping.ListDataFrames(mxd)[0]
		gpo = GpoLegend().path
		gpl = GplLegend().path
		glb = GlbLegend()
		glb_mfl = arcpy.MakeFeatureLayer_management(glb.path, glb.namefc)
		for x in [gpo, gpl, glb.namefc]:
			self.add_layer_to_dataframe(x, mxd, df)		


	def add_layer_to_dataframe(self, obj, mxd, df):
		lyr = arcpy.mapping.Layer(obj)
		lyr.definitionQuery = self.sql
		arcpy.mapping.AddLayer(df, lyr)
		arcpy.RefreshActiveView()



	def runProcess(self):
		classLegend = Legend(self.code, self.sql)
		classLegend.main()
		classAnnotation = Labels(self.code, self.sql)
		classAnnotation.main()
		self.add_all_layers()
		pythonaddins.MessageBox("La generacion de Leyenda Geologica de la hoja ha finalizado satisfactoriamente. \nConsiderar su verificacion y personalizacion. \n \nINGEMMET INC - 2017".format(self.codhoja), "Consideraciones")


	def main(self):
		try:
			self.runProcess()
		except Exception as e:
			pythonaddins.MessageBox("Descripcion: \n{}".format(e), "ERROR")


if __name__ == "__main__":
	poo = MainLegend()
	poo.main()