import sys
sys.path.insert(0, r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\scripts')

from configs.model import *
import arcpy
import pythonaddins
# import os
import string
#import json


arcpy.overwriteOutput = True
arcpy.ImportToolbox(r'\\srvfile01\bdgeocientifica$\Addins_Geoprocesos\MapaGeologico\tbx\CartografiaGeologica_DGR.tbx')




class selectRow(object):
    """Implementation for addin_addin.getRow (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = range(1, 38)
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""
    def onSelChange(self, selection):
        loadCode .disableLoad()
    def onEditChange(self, text):
        loadCode .disableLoad()
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass



class selectCol(object):
    """Implementation for addin_addin.getCol (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = ",".join(string.ascii_uppercase).split(",")
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""
    def onSelChange(self, selection):
        loadCode .disableLoad()
    def onEditChange(self, text):
        loadCode .disableLoad()
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass




class selectQuad(object):
    """Implementation for addin_addin.getQuad (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.items = range(1, 5)
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWW'
        self.value = ""
    def onSelChange(self, selection):
        loadCode .disableLoad()
    def onEditChange(self, text):
        loadCode .disableLoad()
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass



class loadCode(object):
    """Implementation for addin_addin.loadCode (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        codhoja = "{}{}{}".format(getRow.value, getCol.value, getQuad.value)
        if getRow.enabled:
            getRow.enabled = False
            getCol.enabled = False
            getQuad.enabled = False
        else:
            r = pythonaddins.MessageBox("Confirma que desea terminar el proyecto \n en la hoja {}".format(codhoja), "Advertencia", 4)
            if r == u"Yes":
                getRow.enabled = True
                getCol.enabled = True
                getQuad.enabled = True


    def disableLoad(self):
        if getRow.value != "" and getCol.value != "" and getQuad.value != "":
            loadCode.enabled = True
        else:
            loadCode.enabled = False




class makeTableLegend(object):
    """Implementation for addin_addin.TbLegend (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False


    def onClick(self):
        self.errorHandler(self.processDialog())


    def processDialog(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "Tabla de Leyenda Geologica"
            dialog.description = "Generando tabla de Leyenda para su posterior edicion..."
            dialog.animation = "Spiral"
            self.executeProcess()



    def executeProcess(self):
        if getRow.value != "" and getCol.value != "" and getQuad.value != "":
            arcpy.makeTableLegend(getRow.value, getCol.value, getQuad.value)
            pythonaddins.MessageBox("El proceso ha finalizado con exito", "Mensaje")
        else:
            raise RuntimeError("Debe establecer un codigo de hoja correcto")


    def errorHandler(self, function):
         try:
            function
         except Exception as e:
            pythonaddins.MessageBox(e, "ERROR")






class makeFeatureLegend(object):
    """Implementation for addin_addin.Legend (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False


    def onClick(self):
        self.errorHandler()


    def processDialog(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "Leyenda Geologica"
            dialog.description = "Generando Leyenda Geologica..."
            dialog.animation = "Spiral"
            self.executeProcess()



    def executeProcess(self):
        if getRow.value != "" and getCol.value != "" and getQuad.value != "":
            arcpy.makeLegend(getRow.value, getCol.value, getQuad.value)
            pythonaddins.MessageBox("El proceso ha finalizado con exito", "Mensaje")
        else:
            raise RuntimeError("Debe establecer un codigo de hoja correcto")


    def errorHandler(self):
         try:
            self.processDialog()
         except Exception as e:
            pythonaddins.MessageBox(e, "ERROR")



class makeLegendSecond(object):
    """Implementation for addin_addin.LegendSecond (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False


    def onClick(self):
        pass



class makeMap(object):
    """Implementation for addin_addin.MapGeo (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False


    def onClick(self):
        self.errorHandler()


    def processDialog(self):
        with pythonaddins.ProgressDialog as dialog:
            dialog.title = "Tabla de Leyenda Geologica"
            dialog.description = "Generando Mapa Geologico..."
            dialog.animation = "Spiral"
            self.executeProcess()



    def executeProcess(self):
        if getRow.value != "" and getCol.value != "" and getQuad.value != "":
            arcpy.makeMapGeo(getRow.value, getCol.value, getQuad.value)
            pythonaddins.MessageBox("El proceso ha finalizado con exito", "Mensaje")
        else:
            raise RuntimeError("Debe establecer un codigo de hoja correcto")


    def errorHandler(self):
         try:
            self.processDialog()
         except Exception as e:
            pythonaddins.MessageBox(e, "ERROR")



class makeProfile(object):
    """Implementation for addin_addin.Profile (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

