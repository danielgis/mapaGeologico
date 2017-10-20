# -*- coding: utf-8 -*-


import arcpy
import json
import pandas as pd
from configs.model import *
from configs.measure import *
from configs.statics import *
from annotationProcess import *

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = 32718

xyini = [10000, 10000]


class Legend:
    def __init__(self, hoja, sql):
        self.hoja = hoja
        self.hoja100 = hoja[:4]
        self.cuadrante = hoja[-1]
        self.sql = sql
        self.x, self.y = xyini[0], xyini[1]  # MODIFICA LA POSICION DONDE SE CREARA LA LEYENDA
        self.lg = tblegend()
        self.ed = tbage()  # MODULE: configs | file: model
        self.GPOLeyend = GpoLegend()    # model.py
        self.GPLLeyend = GplLegend()    # model.py
        self.GPTLeyend = GptLegend()    # model.py
        self.edad = ColumAge(self.x, self.y)  # MODULE: configs | file: measure
        self.jsonfiles = jsonfiles()  # MODULE: configs | file: statics
        self.containerLines = []


    # ETAPA INICIAL
    # PREPARACION DE INFORMACION


    def dfpandas(self):
        lg = arcpy.da.TableToNumPyArray(self.lg.path, ["*"], self.sql, skip_nulls=False, null_value=-99999)
        ed = arcpy.da.TableToNumPyArray(self.ed.path, ["*"], None, skip_nulls=False, null_value=-99999)
        self.lgdf = pd.DataFrame(lg)
        self.eddf = pd.DataFrame(ed)



    # ETAPA 01
    # CONSTRUCCION DE POLIGONOS DE SIMBOLOGIA - POLIGONOS


    # CREA LA VARIABLE GRUPS PARA IDENTIFICAR SI EXISTEN COLUMNAS A LAS QUE SE LE APLICARA UN ESPACIADO | value = 1
    def getGroup(self):
        grupsTmp = list(self.lgdf[(self.lgdf[self.lg.grupo] != "-99999") | (self.lgdf[self.lg.formacion] != "-99999")][
                            self.lg.tipo].unique())
        self.grups = {1: 0, 2: 0, 3: 0}
        for x in grupsTmp:
            self.grups[x] = 1



    def nroSubcolums(self):
        subcoldf = self.lgdf.sort_values([self.lg.orden])[[self.lg.tipo, self.lg.contform]]
        self.tipos = list(self.lgdf[self.lg.tipo].unique())
        self.tipos.sort()
        controller = 0
        container = []
        current = None
        for i, r in subcoldf.iterrows():
            if r[self.lg.contform] == 1:
                if r[self.lg.tipo] == current:
                    controller = controller + 1
                else:
                    pass
            else:
                controller = 0
            container.append([controller, r[self.lg.tipo]])
            current = r[self.lg.tipo]
        self.subcol = {}
        for x in self.tipos:
            self.subcol[x] = max([m[0] for m in container if m[1] == x]) + 1



    def getCase(self):
        self.simb = simbol(self.x, self.y)
        lim = Coords(self.subcol, self.edad.xfin, self.edad.yfin).getCoord
        if self.tipos in [[1, 2, 3], [1], [1, 2]]:
            C1 = ColUnidLito(self.edad.xfin, self.edad.yfin, lim[1]["xfin"])
            C2 = ColMorfVolc(C1.xfin, C1.yfin, lim[2]["xfin"])
            C3 = ColIntrSubv(C2.xfin, C2.yfin, lim[3]["xfin"])
            self.colums = {1: C1, 2: C2, 3: C3}
        elif self.tipos in [[1, 3]]:
            C1 = ColUnidLito(self.edad.xfin, self.edad.yfin, lim[1]["xfin"])  # MODULE: configs | file: measure
            C3 = ColIntrSubv(C1.xfin, C1.yfin, lim[3]["xfin"])
            self.colums = {1: C1, 3: C3}
        elif self.tipos in [[2, 3]]:
            C2 = ColMorfVolc(self.edad.xfin, self.edad.yfin, lim[2]["xfin"])  # MODULE: configs | file: measure
            C3 = ColIntrSubv(C2.xfin, C2.yfin, lim[3]["xfin"])
            self.colums = {2: C2, 3: C3}



    def delRows(self, geom):
        self.outFc = {"pnt": self.GPTLeyend.path, "lin": self.GPLLeyend.path, "pol": self.GPOLeyend.path}
        with arcpy.da.UpdateCursor(self.outFc[geom], ["OID@"], self.sql) as cursorUC:
            for x in cursorUC:
                cursorUC.deleteRow()
        del cursorUC



    def loadData(self, geom, array):
        feature = {"pnt": self.jsonfiles.gpt, "lin": self.jsonfiles.gpl, "pol": self.jsonfiles.gpo}
        jsonOpen = open(feature[geom], "r")
        jsonLoad = json.load(jsonOpen)
        jsonOpen.close()
        jsonLoad["features"] = array
        json2shp = arcpy.AsShape(jsonLoad, True)
        self.delRows(geom)
        arcpy.Append_management(json2shp, self.outFc[geom], "NO_TEST")
        return json2shp



    # CREA LOS CONTENEDORES DE LOS SIMBOLOS DE LAS FORMACIONES
    # CREA LA VARIABLE simbolPolygon
    def makeForm(self):
        yini = self.simb.yini
        container = []
        tipoCurrent = None
        controller = 1
        k = 0
        cursor = self.lgdf.sort_values([self.lg.orden])
        for i, x in cursor.iterrows():
            xini = self.colums[x[self.lg.tipo]].formc["xini"]

            coords = lambda xini, yini: [[[xini, yini],
                                          [xini, yini + self.simb.heigth],
                                          [xini + self.simb.width, yini + self.simb.heigth],
                                          [xini + self.simb.width, yini],
                                          [xini, yini]]]

            if controller != 1:
                if x[self.lg.contform] == 1:
                    if x[self.lg.tipo] == tipoCurrent:
                        k = k + 1
                        xini = xini + self.simb.contemp[x[self.lg.tipo]] * k
                    else:
                        pass
                else:
                    k = 0
                    yini = yini + self.simb.heigth + self.simb.separ
            else:
                controller = 0

            tipoCurrent = x[self.lg.tipo]

            coordinates = coords(xini, yini)
            rows = {self.lg.codi: x[self.lg.codi],
                    self.lg.codform: None if x[self.lg.codform] == "-99999" else x[self.lg.codform],
                    self.lg.name: x[self.lg.name],
                    self.lg.grupo: None if x[self.lg.grupo] == "-99999" else x[self.lg.grupo],
                    self.lg.formacion: None if x[self.lg.formacion] == "-99999" else x[self.lg.formacion],
                    self.lg.deposito: None if x[self.lg.deposito] == "-99999" else x[self.lg.deposito],
                    self.lg.miembro: None if x[self.lg.miembro] == "-99999" else x[self.lg.miembro],
                    self.lg.cvolc: None if x[self.lg.cvolc] == "-99999" else x[self.lg.cvolc],
                    self.lg.batol: None if x[self.lg.batol] == "-99999" else x[self.lg.batol],
                    self.lg.supuni: None if x[self.lg.supuni] == "-99999" else x[self.lg.supuni],
                    self.lg.unidad: None if x[self.lg.unidad] == "-99999" else x[self.lg.unidad],
                    self.lg.pluton: None if x[self.lg.pluton] == "-99999" else x[self.lg.pluton],
                    self.lg.descrip: x[self.lg.descrip],
                    self.lg.serie: x[self.lg.serie],
                    self.lg.serie_adi: None if x[self.lg.serie_adi] == "-999" else x[self.lg.serie_adi],
                    self.lg.tipo: x[self.lg.tipo],
                    self.lg.contform: None if x[self.lg.contform] == -99999 else x[self.lg.contform],
                    self.lg.orden: x[self.lg.orden],
                    self.lg.hoja: x[self.lg.hoja],
                    self.lg.cuadrante: x[self.lg.cuadrante],
                    self.lg.codhoja: x[self.lg.codhoja]
                    }
            itemFeatures = {"attributes": rows, "geometry": {"rings": coordinates}}
            container.append(itemFeatures)

        self.simbolPolygon = self.loadData("pol", container)




    # ETAPA 02
    # CONSTRUCCION DE COLUMNAS Y DIVISIONES - LINEA


    # OBTIENE LA ALTURA DE LAS SIMBOLOGIAS GENERADAS
    @property
    def getHeigth(self):
        desc = arcpy.Describe(self.simbolPolygon)
        extent = json.loads(desc.extent.JSON)
        # arcpy.AddMessage(type(extent["ymax"]))
        heigth = float(extent["ymax"]) - float(extent["ymin"]) + 250.0
        return heigth



    # CREA LAS COLUMNAS DE ACUERDO A LA OCURRENCIA
    def makeColumns(self):
        self.containerLines = []
        self.h = self.getHeigth
        for k, c in self.colums.items():
            y = c.yTop(self.h)
            coordinates = [[[c.xini, y], [c.xfin, y], [c.xfin, c.yfin], [c.xini, c.yini]]]
            itemFeatures = {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                            "geometry": {"paths": coordinates}}
            self.containerLines.append(itemFeatures)
            head = {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                    "geometry": {"paths": [[[c.xini, y - 550], [c.xfin, y - 550]]]}}
            self.containerLines.append(head)



    def divSerie(self):
        ycontainer = []
        previous = None
        self.datalg = self.lgdf.sort_values(["ORDEN"]).groupby([self.lg.serie, self.lg.serie_adi]).size()
        last = [i for i, x in self.datalg.iloc[[-1]].iteritems()][0]
        for i, x in self.datalg.iteritems():
            sql = "{} = '{}' AND {}".format(self.lg.serie, i[0], self.sql)
            ytmp = max([x[0] for x in arcpy.da.SearchCursor(self.outFc["pol"], ["SHAPE@Y"], sql)])
            y = ytmp if i[1] != "-999" else ytmp + self.simb.elevSerie
            ycontainer.append(y)
            if previous:
                if i[0] != previous:
                    y = ytmp - self.simb.elevSerie
                    ycontainer.append(y)

            if i == last and i[1] == "-999":
                del ycontainer[-1]

            previous = None if i[1] == "-999" else i[1]

        xini = self.edad.serie["xini"]
        xfin = self.edad.serie["xfin"]
        itemFeatures = lambda y: {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                                  "geometry": {"paths": [[[xini, y], [xfin, y]]]}}
        series = map(itemFeatures, ycontainer)
        self.containerLines.extend(series)
        self.divSisEra("eratema")
        self.divSisEra("sistema")
        self.makeColAge("eratema")
        self.makeColAge("sistema")
        self.makeColAge("serie")
        self.makeColAge("edad")
        self.simbolPolyline = self.loadData("lin", self.containerLines)



    def divSisEra(self, edad):
        ycontainer = []
        previous = None
        ages = {"eratema": {
            "xini": self.edad.eratm["xini"],
            "xfin": self.edad.eratm["xfin"]
        },
            "sistema": {
                "xini": self.edad.sistm["xini"],
                "xfin": self.edad.sistm["xfin"]
            }
        }

        lim = 2 if edad == "eratema" else 3
        for i in arcpy.da.SearchCursor(self.outFc["pol"], [self.lg.serie, self.lg.serie_adi, "SHAPE@Y"], self.sql):
            if previous != None:
                if (i[0][0:lim] != previous):
                    y = i[2] - self.simb.elevSerie
                    ycontainer.append(y)
                elif i[1] != None:
                    if (i[0][0:lim] != i[1][0:lim]) and i[1]:
                        y = i[2]
                        ycontainer.append(y)
            else:
                if i[1] != None:
                    if (i[0][0:lim] != i[1][0:lim]) and i[1]:
                        y = i[2]
                        ycontainer.append(y)
            previous = i[1][0:lim] if i[1] != None else i[0][0:lim]

        xini = ages[edad]["xini"]
        xfin = ages[edad]["xfin"]
        itemFeatures = lambda y: {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                                  "geometry": {"paths": [[[xini, y], [xfin, y]]]}}
        series = map(itemFeatures, ycontainer)
        self.containerLines.extend(series)



    def makeColAge(self, ageSelect):
        colums = {
            "eratema": self.edad.eratm,
            "sistema": self.edad.sistm,
            "serie": self.edad.serie,
            "edad": self.edad.edad
        }
        xini = colums[ageSelect]["xini"]
        xfin = colums[ageSelect]["xfin"]
        yini = colums[ageSelect]["yini"]
        yfin = self.edad.yTop(self.h)

        itemFeatures = [{"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                         "geometry": {
                             "paths": [[[xini, yini], [xini, yfin], [xfin, yfin], [xfin, yini], [xini, yini]]]}}]
        self.containerLines.extend(itemFeatures)
        head = {"attributes": {self.lg.codi: 1, self.lg.hoja: self.hoja100, self.lg.cuadrante: self.cuadrante, self.lg.codhoja: self.hoja},
                "geometry": {"paths": [[[xini, yfin - 550], [xfin, yfin - 550]]]}}
        self.containerLines.append(head)



    def main(self):
        self.dfpandas()
        self.nroSubcolums()
        self.getGroup()
        self.getCase()
        self.makeForm()
        self.makeColumns()
        self.divSerie()
        arcpy.RefreshActiveView()