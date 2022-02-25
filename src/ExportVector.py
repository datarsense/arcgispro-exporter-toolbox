# -*- coding: utf-8 -*-

import arcpy
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor
import simplekml

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

        params = [sourcemap, sourcelayer]
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
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map_to_export = aprx.listMaps(parameters[0].value)[0]
        map_to_export.defaultView.exportToPNG('test.png', 1000, 1000)

        ##CSV export
        arcpy.conversion.TableToTable(parameters[1].value, "./", "out.csv")

        ##KML export
        #Reproject featureclass to WGS84
        out_coordinate_system = arcpy.SpatialReference(4326)
        arcpy.env.addOutputsToMap = False
        arcpy.Project_management(parameters[1].value, parameters[1].value.name + "_wgs84", out_coordinate_system)

        #Create a spatially enabled dataframe from featureclass
        sdf = pd.DataFrame.spatial.from_featureclass(parameters[1].value.name + "_wgs84")
        sdf = sdf.drop('OBJECTID', axis=1)

        #Export data to KML
        kml = simplekml.Kml()
        sdf.apply(lambda X: kml.newpoint(name=X["Name"], coords=[( X["SHAPE"]["x"],X["SHAPE"]["y"])]) ,axis=1)
        kml.save(path = "data.kml")

        #Cleanup temporary layer created for reprojection
        arcpy.Delete_management(parameters[1].value.name + "_wgs84")
        return
