import sys
sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')

import arcpy
from configs.settings import *

arcpy.ImportToolbox(Services().FEATURE_TO_POLYGON_SERVICE_TOOLBOX, "FeatureToPolygon_Service")