from unittest import TestCase
from mock import patch, MagicMock
import pandas as pd
import xmltodict
from src.arcgis_exporter import geojson_to_kml

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

        geojson_to_kml(test_data, 'sample2.kml')

        #Test generated XML
        # Open JSON file
        with open('sample2.kml', 'r') as resultkml:
            # Reading from json file
            resultdict = xmltodict.parse(resultkml.read())

            self.assertEqual(resultdict['kml']['Document']['Placemark'][0]['name'], 'Dinagat Islands')
            self.assertEqual(resultdict['kml']['Document']['Placemark'][0]['Point']['coordinates'], '125.6,10.1,0.0')
