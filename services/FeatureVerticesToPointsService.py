import arcpy
import os

FeatureClass = arcpy.GetParameterAsText(0)
PointType = arcpy.GetParameterAsText(1)

try:
	result = arcpy.FeatureVerticesToPoints_management(FeatureClass, os.path.join(arcpy.env.scratchFolder, "MG_POINTS"), PointType)
	arcpy.SetParameterAsText(2, result)
except Exception as e:
	arcpy.AddMessage(e)