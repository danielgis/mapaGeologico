# -*- CODING: UTF-8 -*-

import sys
sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')


from mapgeology import *



class MainMapGeology:
	def __init__(self):
		self.column = arcpy.GetParameterAsText(0)
		self.row = arcpy.GetParameterAsText(1)
		self.quadrant = arcpy.GetParameterAsText(2)
		self.codhoja = FGeneral().codhoja
		self.code = "{}-{}{}".format(self.column, self.row.lower(), self.quadrant)
		self.sql = "{} = '{}'".format(self.codhoja, self.code)


	# IMPLEMENTACION DE CONTROL DE CALIDAD NATES DE RALIZAR EL PROCESAMIENTO DE INFORMACION
	def validation_01(self):
		pass


	def runProcess(self):
		classTableLegend = GenerateMap(self.code, self.sql)
		classTableLegend.main()


	def main(self):
		self.runProcess()


if __name__ == "__main__":
	poo = MainMapGeology()
	poo.main()