import simplekml
import functools

def geojson_to_kml(data, targetpath, namepath, descriptionpath):
    kml = simplekml.Kml()
    for feature in data['features']:
        if feature['geometry']['type'] == 'Polygon':
            kml.newpolygon(name=functools.reduce(dict.get, namepath, feature),
                        description=functools.reduce(dict.get, descriptionpath, feature),
                        outerboundaryis=feature['geometry']['coordinates'][0])
        elif feature['geometry']['type'] == 'LineString':
            kml.newlinestring(name=functools.reduce(dict.get, namepath, feature),
                            description=functools.reduce(dict.get, descriptionpath, feature),
                            coords=feature['geometry']['coordinates'])
        elif feature['geometry']['type'] == 'Point':
            kml.newpoint(name=functools.reduce(dict.get, namepath, feature),
                        description=functools.reduce(dict.get, descriptionpath, feature),
                        coords=[feature['geometry']['coordinates']])
    kml.save(targetpath)
