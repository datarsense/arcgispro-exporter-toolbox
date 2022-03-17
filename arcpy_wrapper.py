import arcpy
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor

def list_workspaces(mxd):
        workspaces = []
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.supports("WORKSPACEPATH"):
                workspaces.append(layer.workspacePath)
        return workspaces

def featureclass_to_geojson(fc):
    #Reproject featureclass to WGS84
    out_coordinate_system = arcpy.SpatialReference(4326)
    arcpy.env.addOutputsToMap = False
    arcpy.Project_management(fc, fc.name + "_wgs84", out_coordinate_system)

    #Create a spatially enabled dataframe from featureclass and convert it to a geojson_data object
    #https://gis.stackexchange.com/questions/418040/converting-arcgis-spatially-enabled-dataframe-to-geojson_data
    sdf = pd.DataFrame.spatial.from_featureclass(fc.name + "_wgs84")
    featureset = sdf.spatial.to_featureset()

    #Cleanup temporary layer created for reprojection
    arcpy.Delete_management(fc.name + "_wgs84")

    return featureset.to_geojson