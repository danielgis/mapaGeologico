import arcpy
import json
import pandas as pd
from configs.model import *
from configs.measure import *
from configs.statics import *
import operator


# IMPORTAR SERVICIOS
arcpy.ImportToolbox(Services().FEATURE_TO_POLYGON_SERVICE_TOOLBOX, "FeatureToPolygon_Service")
arcpy.ImportToolbox(Services().FEATURE_VERTICES_TO_POINT_SERVICE_TOOLBOX, "FeatureVerticesToPointService")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::: ETA 01 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# CONSTRUCCION DE ETIQUETAS A BASE DE PUNTOS REFERENCIADOS
xyini = [10000, 10000]


# ETIQUETAS CABECERA
class Labels:
    def __init__(self, hoja, sql):
        self.hoja = hoja
        self.hoja100 = hoja[:4]
        self.cuadrante = hoja[-1]
        self.sql = sql
        self.gpo = GpoLegend()
        self.gpl = GplLegend()
        self.gpt = GptLegend()
        self.glb = GlbLegend()
        self.GEOJSON = jsonfiles()
        self.gptJSON = self.GEOJSON.gpt
        self.tabla_leyenda = tblegend()
        self.tabla_edades = tbage()
        self.columna_edades = ColumAge(xyini[0], xyini[1])
        self.label = Annotation()  # STATICS FILES
        self.container = []



    def dframes(self):
        celdas_flayer = arcpy.MakeFeatureLayer_management(self.gpl.path, "celdas_flayer", self.sql)
        #self.pol = arcpy.FeatureToPolygon_management(celdas_flayer, "in_memory\polygon")
        self.pol = arcpy.FeatureToPolygon_Service.test(celdas_flayer)   # USE SERVICE
        #celdas_vertices_end = arcpy.FeatureVerticesToPoints_management(celdas_flayer, 'in_memory\celdas_vEnd', 'END')
        celdas_vertices_end = arcpy.FeatureVerticesToPointService.FeatureVerticesToPointService(celdas_flayer, 'END')    # USE SERVICE



        shapefile_to_dataframe_01 = arcpy.da.FeatureClassToNumPyArray(self.pol, ["SHAPE@X", "SHAPE@Y"])
        self.dframe_centroide = pd.DataFrame(shapefile_to_dataframe_01)  # CENTROIDES


        shapefile_to_dataframe_02 = arcpy.da.TableToNumPyArray(self.tabla_leyenda.path, ["*"], self.sql,
                                                               skip_nulls=False, null_value=-99999)
        self.dframe_leyenda = pd.DataFrame(shapefile_to_dataframe_02)  # TB LEYENDA


        shapefile_to_dataframe_03 = arcpy.da.TableToNumPyArray(self.tabla_edades.path, ["*"], None, skip_nulls=False,
                                                               null_value=-99999)
        self.dframe_edades = pd.DataFrame(shapefile_to_dataframe_03)  # TB EDADES


        shapefile_to_dataframe_04 = arcpy.da.FeatureClassToNumPyArray(celdas_vertices_end, ["SHAPE@X", "SHAPE@Y"])
        self.dframe_vertice_final_edad = pd.DataFrame(shapefile_to_dataframe_04)  # DATA FRAME DE VERTICES FINALES DE EDADES


        shapefile_to_dataframe_05 = arcpy.da.FeatureClassToNumPyArray(self.gpo.path, [self.gpo.orden, self.gpo.tipo,
                                                                                      self.gpo.descrip, self.gpo.grupo,
                                                                                      self.gpo.formacion,
                                                                                      self.gpo.deposito,
                                                                                      self.gpo.miembro,
                                                                                      self.gpo.cvolc, self.gpo.batol,
                                                                                      self.gpo.supuni, self.gpo.unidad,
                                                                                      self.gpo.pluton, "SHAPE@X",
                                                                                      "SHAPE@Y"], self.sql)
        self.dframe_gpo_leyenda = pd.DataFrame(shapefile_to_dataframe_05)



    @property
    def heigthCeld(self):
        desc = arcpy.Describe(self.pol)
        extent = json.loads(desc.extent.JSON)
        y = {"ymax": extent["ymax"], "ymin": extent["ymin"]}
        return y



    def delRows(self, feature):
        mfl = arcpy.MakeFeatureLayer_management(feature, "mfl", self.sql)
        E = arcpy.da.Editor(Conexion().conn)
        E.startEditing(True, True)
        arcpy.DeleteRows_management(mfl)
        E.stopEditing(True)



    def loadData(self):
        jsonOpen = open(self.gptJSON, "r")
        jsonLoad = json.load(jsonOpen)
        jsonOpen.close()
        jsonLoad["features"] = self.container
        json2shp = arcpy.AsShape(jsonLoad, True)
        self.delRows(self.gpt.path)
        self.delRows(self.glb.path)
        arcpy.Append_management(json2shp, self.gpt.path, "NO_TEST")
        self.add_codhoja_annotation()



    def add_codhoja_annotation(self):
        rows = [x[0] for x in arcpy.da.SearchCursor(self.gpt.path, ["OID@"], self.sql)]
        sqlClause = "FeatureID IN ({})".format(", ".join([str(x) for x in rows]))
        with arcpy.da.UpdateCursor(self.glb.path, [self.gpt.codhoja, self.glb.hoja, self.glb.cuadrante], sqlClause) as cursorUC:
            for x in cursorUC:
                x[0], x[1], x[2] = self.hoja, self.hoja100, self.cuadrante
                cursorUC.updateRow(x)
        del cursorUC



    def labelHead(self):
        y = self.heigthCeld
        centroide_head = self.dframe_centroide[(self.dframe_centroide["SHAPE@Y"] <= y["ymax"]) &
                                               (self.dframe_centroide["SHAPE@Y"] >= y["ymax"] - 550)].sort_values(["SHAPE@X"])

        centroide_head.reset_index(level=0, inplace=True)
        types = list(self.dframe_leyenda[self.tabla_leyenda.tipo].unique())
        types.sort()

        for i, v in centroide_head[:4].iterrows():
            itemFeatures = [{"attributes": {self.gpt.nombre: self.label.head_age_label[i + 1],
                                            self.gpt.estilo: self.label.headClass["ages"], self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante, self.gpt.codhoja: self.hoja}, 
                                            "geometry": {"x": float(v["SHAPE@X"]), "y": float(v["SHAPE@Y"])}}]

            self.container.extend(itemFeatures)

        for i, v in centroide_head[4:].iterrows():
            itemFeatures = [{"attributes": {self.gpt.nombre: self.label.head_column_label[types[i - 4]],
                                            self.gpt.estilo: self.label.headClass["colum"], self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante,
                                            self.gpt.codhoja: self.hoja}, "geometry": {"x": float(v["SHAPE@X"]), "y": float(v["SHAPE@Y"])}}]

            self.container.extend(itemFeatures)



    def get_edades_label(self, edad):
        serie_row = list(self.dframe_leyenda[self.tabla_leyenda.serie].unique())
        serieadi_row_tmp = list(self.dframe_leyenda[self.tabla_leyenda.serie_adi].unique())
        serieadi_row = [x for x in serieadi_row_tmp if x != "-999"]
        serie_row.extend(serieadi_row)

        annotation_age = list(set(serie_row))
        if edad == "sistema":
            annotation_age = list(set([x[:3] for x in annotation_age]))
        elif edad == "eratema":
            annotation_age = list(set([x[:2] for x in annotation_age]))
        elif edad == "edad":
            pass

        dframe_edad = self.dframe_edades[self.dframe_edades[self.tabla_edades.id_edad].isin(annotation_age)]
        result = list(dframe_edad[self.tabla_edades.nombre]) if edad != "edad" else list(dframe_edad[self.tabla_edades.edad_ini])
        return result



    def labelAge(self, edad):

        y = self.heigthCeld

        columns = {
            "eratema": self.columna_edades.eratm,
            "sistema": self.columna_edades.sistm,
            "serie": self.columna_edades.serie,
        }
        xmax = columns[edad]["xfin"]
        xmin = columns[edad]["xini"]
        centroide_age = self.dframe_centroide[(self.dframe_centroide["SHAPE@Y"] <= y["ymax"] - 550) &
                                              (self.dframe_centroide["SHAPE@Y"] >= y["ymin"]) &
                                              (self.dframe_centroide["SHAPE@X"] <= xmax) &
                                              (self.dframe_centroide["SHAPE@X"] >= xmin)].sort_values(["SHAPE@Y"])

        centroide_age.reset_index(level=0, inplace=True)

        edades = self.get_edades_label(edad)
        for i, v in centroide_age.iterrows():
            itemFeatures = [{"attributes": {self.gpt.nombre: edades[i], self.gpt.estilo: self.label.laterClass[edad], 
                                            self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante,
                                            self.gpt.codhoja: self.hoja},
                             "geometry": {"x": float(v["SHAPE@X"]), "y": float(v["SHAPE@Y"])}}]
            self.container.extend(itemFeatures)



    def labelAgeNum(self):
        y = self.heigthCeld
        xmax = self.columna_edades.edad["xfin"]
        xmin = self.columna_edades.edad["xini"]
        vertices_edades = self.dframe_vertice_final_edad[(self.dframe_vertice_final_edad["SHAPE@Y"] < y["ymax"] - 650) &
                                                         (self.dframe_vertice_final_edad["SHAPE@Y"] > y["ymin"]) &
                                                         (self.dframe_vertice_final_edad["SHAPE@X"] < xmax) &
                                                         (self.dframe_vertice_final_edad["SHAPE@X"] > xmin)].sort_values(["SHAPE@Y"])

        vertices_edades.reset_index(level=0, inplace=True)
        edades = self.get_edades_label("edad")

        for i, v in vertices_edades.iterrows():
            itemFeatures = [{"attributes": {self.gpt.nombre: edades[i],
                                            self.gpt.estilo: self.label.laterClass["edad"], self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante,
                                            self.gpt.codhoja: self.hoja},
                                            "geometry": {"x": float(v["SHAPE@X"]), "y": float(v["SHAPE@Y"])}}]

            self.container.extend(itemFeatures)




    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::: ETIQUETAS COLUMNA 01 ::::::::::::::::::::::::::::::::::::::::::::::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def agregar_valores_array(self, dframe, componente, x, oper=None):
        for i, v in dframe.iteritems():
            if oper:
                txt = "|".join(i.split(" ")) if oper == 2 else i
            else:
                txt = i
            itemFeatures = [{"attributes": {self.gpt.nombre: txt,
                                            self.gpt.estilo: self.label.annotationClass[componente], self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante,
                                            self.gpt.codhoja: self.hoja},
                                            "geometry": {"x": x, "y": float(v)}}]
            self.container.extend(itemFeatures)



    def componentes_unidades_litoest_label(self, x, estilo, componente):
        query_data_frame = self.dframe_gpo_leyenda[self.dframe_gpo_leyenda[componente] != "None"].groupby(componente)["SHAPE@Y"].mean()
        if query_data_frame.size != 0:
            self.agregar_valores_array(query_data_frame, estilo, x)



    def formacion_unidades_litoest_label(self, x, oper):
        operacion = {1: operator.eq, 2: operator.ne}
        query_data_frame = self.dframe_gpo_leyenda[(self.dframe_gpo_leyenda[self.gpo.formacion] != "None") &
                                                   (operacion[oper](self.dframe_gpo_leyenda[self.gpo.miembro], "None"))].groupby(self.gpo.formacion)["SHAPE@Y"].mean()

        if query_data_frame.size != 0:
            self.agregar_valores_array(query_data_frame, "formacion_deposito", x, oper=oper)



    def unidades_litoestatigraficas_label(self, process):
        add = Annot_unidades_litoestatigraficas()
        if process:
            xtmp = list(self.dframe_gpo_leyenda[(self.dframe_gpo_leyenda[self.gpo.tipo] == 1)].groupby(self.gpo.grupo)["SHAPE@X"].min())
            x_grupo = min(xtmp) + add.distancia_grupo
            self.componentes_unidades_litoest_label(x_grupo, "grupo", self.gpo.grupo)
            x_formacion = min(xtmp) + add.distancia_formacion_deposito
            for oper in range(1, 3):
                self.formacion_unidades_litoest_label(x_formacion, oper)
            self.componentes_unidades_litoest_label(x_formacion, "formacion_deposito", self.gpo.deposito)
            x_miembro = min(xtmp) + add.distancia_miembro
            self.componentes_unidades_litoest_label(x_miembro, "miembro", self.gpo.miembro)
        else:
            pass



    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::: ETIQUETAS COLUMNA 02 ::::::::::::::::::::::::::::::::::::::::::::::::::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def conjunto_volcanico_morfoestructuras_volcanicas_label(self, x):
        query_data_frame = \
        self.dframe_gpo_leyenda[self.dframe_gpo_leyenda[self.gpo.cvolc] != "None"].groupby(self.gpo.cvolc)["SHAPE@Y"].mean()
        if query_data_frame.size != 0:
            self.agregar_valores_array(query_data_frame, "conjunto_volcanico", x)



    def morfoestructuras_volcanicas_label(self, process):
        add = Annot_morfoestructuras_volcanicas()
        if process:
            xtmp = list(self.dframe_gpo_leyenda[(self.dframe_gpo_leyenda[self.gpo.tipo] == 2)].groupby(self.gpo.cvolc)["SHAPE@X"].min())
            x_cvolc = min(xtmp) + add.distancia_conjunto_volcanico
            self.conjunto_volcanico_morfoestructuras_volcanicas_label(x_cvolc)
        else:
            pass


    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::: ETIQUETAS COLUMNA 03 ::::::::::::::::::::::::::::::::::::::::::::::::::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def componentes_intrusivos_subvolcanicos_label(self, x, estilo, componente):
        query_data_frame = self.dframe_gpo_leyenda[self.dframe_gpo_leyenda[componente] != "None"].groupby(componente)["SHAPE@Y"].mean()
        if query_data_frame.size != 0:
            self.agregar_valores_array(query_data_frame, estilo, x)



    def intrusivos_subvolcanicos_label(self, process):
        add = Annot_rocas_intrusivas_subvolcanicas()
        if process:
            xtmp = list(self.dframe_gpo_leyenda[(self.dframe_gpo_leyenda[self.gpo.tipo] == 3)].groupby(self.gpo.batol)["SHAPE@X"].min())
            x_batolito = min(xtmp) + add.distancia_batolito
            self.componentes_intrusivos_subvolcanicos_label(x_batolito, "batolito", self.gpo.batol)
            x_super_unidad = min(xtmp) + add.distancia_super_unidad
            self.componentes_intrusivos_subvolcanicos_label(x_super_unidad, "super_unidad", self.gpo.supuni)
            x_unidad = min(xtmp) + add.distancia_unidad
            self.componentes_intrusivos_subvolcanicos_label(x_unidad, "unidad", self.gpo.unidad)
            x_pluton = min(xtmp) + add.distancia_pluton
            self.componentes_intrusivos_subvolcanicos_label(x_pluton, "pluton", self.gpo.pluton)
        else:
            pass


    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::: ETIQUETAS COLUMNAS - JSON2FC  ::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    @property
    def obtener_columnas_existentes(self):
        col = list(self.dframe_gpo_leyenda[self.gpo.tipo].unique())
        col.sort()
        result = {1: None, 2: None, 3: None}
        for x in col:
            result[x] = x
        return result



    def anotaciones_adicionales(self):
        ctrl = self.obtener_columnas_existentes
        self.unidades_litoestatigraficas_label(ctrl[1])
        self.morfoestructuras_volcanicas_label(ctrl[2])
        self.intrusivos_subvolcanicos_label(ctrl[3])



    def rango_maximo_caracteres_por_linea(self, txt, num_max_caracter):
        array_palabras = txt.split(" ")
        array_palabras_agrupadas = []
        while len(array_palabras) > 0:
            acum = 0
            tmp = []
            while acum <= num_max_caracter and len(array_palabras) > 0:
                acum = acum + len(array_palabras[0]) + 1
                if acum < num_max_caracter:
                    tmp.append(array_palabras[0])
                    del array_palabras[0]
                else:
                    break
            array_palabras_agrupadas.append(tmp)

        result = "|".join([" ".join(x) for x in array_palabras_agrupadas])
        return result



    def descripcion_label(self):
        add = Annot_unidades_litoestatigraficas()
        distancia_al_centroide = add.distancia_descripcion
        for i, v in self.dframe_gpo_leyenda.iterrows():
            txt = v[self.gpo.descrip]
            if v[self.gpo.tipo] in (1, 2):
                desc = self.rango_maximo_caracteres_por_linea(txt, 60)
            elif v[self.gpo.tipo] == 3:
                desc = self.rango_maximo_caracteres_por_linea(txt, 52)

            itemFeatures = [{"attributes": {self.gpt.nombre: desc,
                                            self.gpt.estilo: self.label.annotationClass["descripcion"], self.gpt.hoja: self.hoja100, self.gpt.cuadrante: self.cuadrante,
                                            self.gpt.codhoja: self.hoja},
                                            "geometry": {"x": float(v["SHAPE@X"]) + distancia_al_centroide, "y": float(v["SHAPE@Y"])}}]
            self.container.extend(itemFeatures)

    def main(self):
        self.dframes()
        self.labelHead()
        self.labelAge("eratema")
        self.labelAge("sistema")
        self.labelAge("serie")
        self.labelAgeNum()
        self.descripcion_label()
        self.anotaciones_adicionales()
        self.loadData()
        arcpy.RefreshActiveView()