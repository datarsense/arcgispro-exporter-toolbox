from unittest import TestCase
from mock import patch, MagicMock
import xmltodict
import os
from arcgis_exporter import geojson_to_kml

class TestArcgisExporter(TestCase):
    def test_geojson_to_kml(self):
        test_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [125.6, 10.1]
                    },
                    "properties": {
                        "name": "Dinagat Islands"
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [125.6, 10.1]
                    },
                    "properties": {
                        "name": "Tangu Airport"
                    }
                }
            ]
        }

        geojson_to_kml(test_data, 'sample.kml')

        #Test generated XML
        # Open JSON file
        with open('sample.kml', 'r') as resultkml:
            # Reading from json file
            resultdict = xmltodict.parse(resultkml.read())

            self.assertEqual(resultdict['kml']['Document']['Placemark'][0]['name'], 'Dinagat Islands')
            self.assertEqual(resultdict['kml']['Document']['Placemark'][0]['Point']['coordinates'], '125.6,10.1,0.0')

        os.remove('sample.kml')
