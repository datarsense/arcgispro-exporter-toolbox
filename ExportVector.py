# -*- coding: utf-8 -*-

import arcpy
import json
import arcpy_wrapper
import arcgis_exporter

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [SingleVectorExporter, MapExporter]

class SingleVectorExporter(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export single vector"
        self.description = "Export single vector"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        sourcelayer = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        params = [sourcelayer]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        selectedvectors = [row for row in arcpy.da.SearchCursor(parameters[0].value, '*')] #arcpy.SearchCursor(parameters[0].value)
        if len(selectedvectors) == 0 :
            arcpy.AddError("No vector has been selected")
        elif len(selectedvectors) > 1:
            arcpy.AddError("Multiple or no vectors have been selected. Unable to export data")
        else:
            arcpy.AddMessage(selectedvectors[0])
        return

class MapExporter(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export map and vectors"
        self.description = "Export map and vectors"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        sourcemap = arcpy.Parameter(
            displayName="Map",
            name="in_map",
            datatype="GPMap",
            parameterType="Required",
            direction="Input")

        sourcelayer = arcpy.Parameter(
            displayName="Vector layer",
            name="in_featurelayer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        namefield = arcpy.Parameter(
            displayName="KML name field",
            name="in_namefield",
            datatype="GPString",
            parameterType="Required",
            enabled=False,
            direction="Input")
        namefield.filter.type = "ValueList"
        namefield.filter.list = []

        descriptionfield = arcpy.Parameter(
            displayName="KML description field",
            name="in_descriptionfield",
            datatype="GPString",
            parameterType="Required",
            enabled=False,
            direction="Input")
        namefield.filter.type = "ValueList"
        namefield.filter.list = []

        params = [sourcemap, sourcelayer, namefield, descriptionfield]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # if the input table view is changed
        if parameters[1].altered:
            inputTable = parameters[1].value

            # Iterate through the fields
            fieldlist = []
            for field in arcpy.ListFields(inputTable):
                fieldlist.append(field.name)
            
            parameters[2].filter.list = fieldlist
            parameters[2].enabled = True

            parameters[3].filter.list = fieldlist
            parameters[3].enabled = True
 
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        ##MAP export as PNG file
        self.map_to_png(parameters[0].value, 'test.png', 1000, 1000)

        ##CSV export
        self.featureclass_to_csv(parameters[1].value, "./", "out.csv")

        ##KML export
        self.featureclass_to_kml(parameters[1].value, "data.kml", parameters[2].value, parameters[3].value)
        
    
    def map_to_png(self, map, targetpath, width, height):
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map_to_export = aprx.listMaps(map)[0]
        map_to_export.defaultView.exportToPNG(targetpath, width, height)

    def featureclass_to_csv(self, fc, directory, filename):
        arcpy.conversion.TableToTable(fc, directory, filename)

    def featureclass_to_kml(self, fc, targetpath, kmlobjectnamefield, kmlobjectdescfield):
        #Export feature class to a geojson object
        geojson_data = json.loads(arcpy_wrapper.featureclass_to_geojson(fc))

        #Business function converting geojson data to KML
        arcgis_exporter.geojson_to_kml(geojson_data, targetpath, kmlobjectnamefield, kmlobjectdescfield)
