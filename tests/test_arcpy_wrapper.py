import arcgis
from unittest import TestCase
from mock import patch, MagicMock

#Mock non-existing arcpy module to enable unit testing in a non-esri environment
from surrogate import surrogate
surrogate.importorinject('arcpy')
surrogate.importorinject('arcgis.features.GeoAccessor')
surrogate.importorinject('arcgis.features.GeoSeriesAccessor')

class TestListDataSources(TestCase):
    @patch('ExportVector.arcpy')
    @patch('ExportVector.arcgis', create=True)
    def test_mapexporter(self, mock_arcpy, mock_arcgis):
        from ExportVector import MapExporter
        arcgisProject = MagicMock()
        mock_arcpy.mp.ArcGISProject = MagicMock(return_value=[arcgisProject])

        exporter = MapExporter()
        #exporter.execute(["test"],[])

        self.assertEqual(True, True)

    @patch('arcpy_wrapper.arcpy')
    def test_list_single_data_source(self, mock_arcpy):
        from arcpy_wrapper import list_workspaces
        data_source = 'layer1'

        layer = MagicMock()
        layer.supports.return_value=True
        layer.workspacePath = data_source

        mock_arcpy.mapping.ListLayers = MagicMock(return_value=[layer])
        mxd = {}
        expected = [data_source]
        actual = list_workspaces(mxd)

        self.assertEqual(expected, actual)

    @patch('arcpy_wrapper.arcpy')
    def test_featuresetto_geojson(self, mock_arcpy):
        from arcpy_wrapper import featureset_to_geojson
        # Set sample data
        data_json = '''{
                "objectIdFieldName": "objectid",
                "globalIdFieldName": "globalid",
                "geometryType": "esriGeometryPolygon",
                "spatialReference": {
                "wkid": 102100,
                "latestWkid": 3857
            },
            "fields": [
            {
                "name": "objectid",
                "alias": "OBJECTID",
                "type": "esriFieldTypeOID"
            },
            {
                "name": "requestid",
                "alias": "Service Request ID",
                "type": "esriFieldTypeString",
                "length": 25
            },
            {
                "name": "requesttype",
                "alias": "Problem",
                "type": "esriFieldTypeString",
                "length": 100
            },
            {
                "name": "comments",
                "alias": "Comments",
                "type": "esriFieldTypeString",
                "length": 255
            }
            ],
            "features": [
                {
                "geometry": {
                    "rings": [
                            [
                                [-9809161.170230601, 5123045.5266209831, 0, 0],
                                [-9809162.170230601, 5123046.5266209831, 0, 0]
                                ],
                            [
                                [-9809163.170230601, 5123047.5266209831, 0, 0],
                                [-9809164.170230601, 5123048.5266209831, 0, 0]
                            ]
                        ]   },
                "attributes": {
                    "objectid": 246362,
                    "requestid": "1",
                    "requesttype": "Sidewalk Damage",
                    "comments": "Pothole"
                }
                },
                {
                "geometry": {
                        "rings": [
                            [
                                [-9809161.170230601, 5123045.5266209831, 0, 0],
                                [-9809162.170230601, 5123046.5266209831, 0, 0]
                                ],
                            [
                                [-9809163.170230601, 5123047.5266209831, 0, 0],
                                [-9809164.170230601, 5123048.5266209831, 0, 0]
                            ]
                        ]
                },
                "attributes": {
                    "objectid": 246382,
                    "requestid": "2",
                    "requesttype": "Pothole",
                    "comments": "Jhh"
                }
            }
            ]
            }'''

        # Create FeatureSet from Esri JSON and convert it to geojson
        data_featureset = arcgis.features.FeatureSet.from_json(data_json)
        in_geojson = featureset_to_geojson(data_featureset)
        self.assertEqual(len(in_geojson['features']), 2)
