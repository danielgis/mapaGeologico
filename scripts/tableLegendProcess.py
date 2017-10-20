import arcpy
import json
from configs.model import *

arcpy.env.overwriteOutput = True

class TableLegend:
	def __init__(self, hoja, sql):
		self.hoja = hoja
		self.hoja100 = "{}-{}".format(hoja[:2], hoja[-2])
		arcpy.AddMessage(self.hoja100)
		self.cuad = GpoHojas100()
		self.zone = [x[0] for x in arcpy.da.SearchCursor(self.cuad.path, [self.cuad.zonageo], "{} = '{}'".format(self.cuad.codhoja, self.hoja100))][0]
		self.geo = GpoGeology(self.zone)
		self.legend = tblegend()
		self.sql = sql
		self.eqField = {
						"FIRST_{}".format(self.geo.codi): self.geo.codi,
						"FIRST_{}".format(self.geo.codform): self.geo.codform,
						"FIRST_{}".format(self.geo.hoja): self.geo.hoja,
						"FIRST_{}".format(self.geo.cuadrante): self.geo.cuadrante,
						"FIRST_{}".format(self.geo.codhoja): self.geo.codhoja
					   }
		self.paramsProp = "{} FIRST;{} FIRST;{} FIRST;{} FIRST;{} FIRST".format(self.geo.codi, self.geo.codform, self.geo.hoja, self.geo.cuadrante, self.geo.codhoja)


	@property
	def exists(self):
		self.mfl = arcpy.MakeFeatureLayer_management(self.geo.path, "Geology_mfl", self.sql)
		if int(arcpy.GetCount_management(self.mfl)[0]) == 0:
			return False
		else:
			return True


	def getTable(self):
		self.stats = arcpy.Statistics_analysis(self.mfl, "tbLegend_tmp", self.paramsProp, self.geo.name)
		for k, v in self.eqField.items():
			arcpy.AlterField_management(self.stats, k, v)



	def delRows(self):
		with arcpy.da.UpdateCursor(self.legend.path, ["OID@"], self.sql) as cursorUC:
			for x in cursorUC:
				cursorUC.deleteRow()
		del cursorUC
		


	def loadData(self):
		arcpy.Append_management(self.stats, self.legend.path, "NO_TEST")



	def viewTable(self):
		mxd = arcpy.mapping.MapDocument("CURRENT")
		df = arcpy.mapping.ListDataFrames(mxd)[0]
		nameTb = os.path.basename(self.legend.path)
		tbLyr = arcpy.mapping.ListTableViews(mxd, nameTb, df)
		if len(tbLyr) > 0:
			tbview = tbLyr[0]
		else:
			tbview = arcpy.mapping.TableView(self.legend.path)
		tbview.definitionQuery = self.sql
		arcpy.mapping.AddTableView(df, tbview)
		arcpy.RefreshActiveView()
		del mxd



	def main(self):
		try:
			if self.exists:
				self.getTable()
				self.delRows()
				self.loadData()
				self.viewTable()
			else:
				raise RuntimeError("\n  El codigo consultado no existe...\n")
		except Exception as e:
			arcpy.AddWarning(e)
