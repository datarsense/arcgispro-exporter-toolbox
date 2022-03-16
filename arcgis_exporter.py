import simplekml

def geojson_to_kml(data, targetpath):
    kml = simplekml.Kml()
    for feature in data['features']:
        if feature['geometry']['type'] == 'Polygon':
            kml.newpolygon(name=feature['properties']['name'],
                        description='test',
                        outerboundaryis=feature['geometry']['coordinates'][0])
        elif feature['geometry']['type'] == 'LineString':
            kml.newlinestring(name=feature['properties']['name'],
                            description='test',
                            coords=feature['geometry']['coordinates'])
        elif feature['geometry']['type'] == 'Point':
            kml.newpoint(name=feature['properties']['name'],
                        description='test',
                        coords=[feature['geometry']['coordinates']])
    kml.save(targetpath)
