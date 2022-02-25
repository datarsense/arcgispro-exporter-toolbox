from unittest import TestCase
from mock import patch, MagicMock

#Mock non-existing arcpy module to enable unit testing in a non-esri environment
from surrogate import surrogate
surrogate.importorinject('arcpy')
surrogate.importorinject('arcgis.features.GeoAccessor')
surrogate.importorinject('arcgis.features.GeoSeriesAccessor')

class TestListDataSources(TestCase):
    @patch('src.ExportVector.arcpy')
    @patch('src.ExportVector.arcgis', create=True)
    def test_mapexporter(self, mock_arcpy, mock_arcgis):
        from src.ExportVector import MapExporter
        arcgisProject = MagicMock()
        mock_arcpy.mp.ArcGISProject = MagicMock(return_value=[arcgisProject])

        exporter = MapExporter()
        exporter.execute(["test"],[])

        self.assertEqual(True, True)

    @patch('arcpy_wrapper.list_workspaces_for_mxd.arcpy')
    def test_list_single_data_source(self, mock_arcpy):
        from arcpy_wrapper import list_workspaces_for_mxd
        data_source = 'layer1'

        layer = MagicMock()
        layer.supports.return_value=True
        layer.workspacePath = data_source

        mock_arcpy.mapping.ListLayers = MagicMock(return_value=[layer])
        mxd = {}
        expected = [data_source]
        actual = list_workspaces_for_mxd.list_workspaces(mxd)

        self.assertEqual(expected, actual)