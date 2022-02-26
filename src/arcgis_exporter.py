import simplekml

def spatialdataframe_to_kml(sdf, targetpath):
    sdf = sdf.drop('OBJECTID', axis=1)
    kml = simplekml.Kml()
    sdf.apply(lambda X: kml.newpoint(name=X["Name"], coords=[( X["SHAPE"]["x"],X["SHAPE"]["y"])]) ,axis=1)
    kml.save(path = targetpath)