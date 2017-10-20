import arcpy
import os

FeatureClass = arcpy.GetParameterAsText(0)

try:
	result = arcpy.FeatureToPolygon_management(FeatureClass, os.path.join(arcpy.env.scratchFolder, "MG_POLYGON"))
	arcpy.SetParameterAsText(1, result)
except Exception as e:
	arcpy.AddMessage(e)