import arcpy
import json
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor

def list_workspaces(mxd):
        workspaces = []
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.supports("WORKSPACEPATH"):
                workspaces.append(layer.workspacePath)
        return workspaces

# Export Arcgis featureclass to feature set and optionnally reproject it to target SR
def featureclass_to_featureset(fc: str, sr: int=None) -> arcpy.FeatureSet:
    #Create a spatially enabled dataframe from featureclass and convert it to a geojson_data object
    #https://gis.stackexchange.com/questions/418040/converting-arcgis-spatially-enabled-dataframe-to-geojson_data
    sdf = pd.DataFrame.spatial.from_featureclass(fc)

    if sr is not None:
        #Project arcpy.geometry objects to target SpatialReference
        sdf.dropna(inplace=True)
        out_coordinate_system = arcpy.SpatialReference(sr)
        sdf['SHAPE'] = sdf['SHAPE'].apply(lambda x: x.project_as(out_coordinate_system))

    return sdf.spatial.to_featureset()

def featureset_to_geojson(fs: arcpy.FeatureSet) -> dict:
    return json.loads(fs.to_geojson)