def hawkid():
    return(["A H M Mainul Islam", "ahmmislam"])

# import the system module

import arcpy
import os
arcpy.env.overwriteOutput = True

def calculateDensity(fcPolygon, attribute, geodatabase):

    import arcpy
    import os
    arcpy.env.overwriteOutput = True

    # setting up the workspace
    arcpy.env.workspace = geodatabase

    # List feature classes
    fcList = arcpy.ListFeatureClasses()

    # Checking if the feature class is in the geodatabase
    if fcPolygon not in fcList:
        print(fcPolygon + " does not exist in the geodatabase")
    else:
        print(fcPolygon + " exists in geodatabase")

    describe_fc = arcpy.Describe(fcPolygon)

    # checking the shapetype of the polygon
    if describe_fc.shapeType == "Polygon":
        print(fcPolygon + " is a polygon")
    else:
        print(fcPolygon + " is not a polygon")

    # checking attributes
    fields = [f.name for f in arcpy.ListFields(fcPolygon)]

    if attribute not in fields:
        print("Attribute of " + fcPolygon + "-" + attribute + " is not in the list of field names")
    else:
        print("Attribute of " + fcPolygon + "-" + attribute + " is in the list of field names")

    # check the coordinate systems and units
    check_coordinate = arcpy.Describe(fcPolygon).spatialReference.linearUnitName

    if check_coordinate == "Meter" and "Feet":
        print("Good to go: area calculations are accurate in geographic coordinate systems!")
    else:
        print("Warning: area calculations are not accurate in geographic coordinate systems!")

    # adding field to the fcPolygon
    arcpy.AddField_management(fcPolygon, "area_sqm", "DOUBLE")

    # calculate geomtery attributes
    arcpy.CalculateGeometryAttributes_management(fcPolygon, [["area_sqm", "AREA"]], "METERS", "SQUARE_METERS")

    # adding field
    arcpy.AddField_managment(fcPolygon, "density_sqm", "FLOAT")

    # calculating the fields
    arcpy.management.CalculateField(fcPolygon, "density_sqm", "!DP0010001!/!areasqm!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

#### def calculateDensity("census2010_counties", "DP0010001", "hw5.gdb")

def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase):

    # setting up the work environment
    arcpy.env.workspace = geodatabase

    # list feature classes
    fcList = arcpy.ListFeatureClasses()

    # checking the existance of the polyline file in the geodatabase
    if fcLine not in fcList:
        print(fcLine + " does not exist in the geodatabase")
    else:
        print(fcLine + " exists in the geodatabase")

    # checking the shapetype of features
    describe_fc = arcpy.Describe(fcLine)

    if describe_fc.ShapeType == "Polyline":
        print(fcLine + " is a polyline")
    else:
        print(fcLine + " is not a polyline")

    # polygon check
    fcPolygon = "states48_albers"
    fields = [f.name for f in arcpy.ListFields(fcPolygon)]

    attribute = "STATE_FIPS"

    if attribute not in fields:
        print("Attribute of " + fcLine + "-" + attribute + " is not in the list of field names")
    else:
        print("Attribute of " + fcLine + "-"+ attribute + " is in the list of field names")

    # checking the coordinates
    check_Coordinate_fcl = arcpy.Describe(fcLine).spatialReference.Name
    check_Coordinate_fcp = arcpy.Describe(fcPolygon).spatialReference.Name

    if check_Coordinate_fcl is not check_Coordinate_fcp:
        print ("The coordinate systems are not same. Shapefile without projected coordinate systems need to be projected to continue analysis.")
        fcLine_Projected = "fcLine_Projected"
        arcpy.Project_management(fcLine, fcLine_Projected, arcpy.Describe(fcPolygon).spatialReference)

    if fcLine_Projected not in fcList:
        print("Projection failed. Try again! Make sure to use the right output coordinate system!")
    else:
        print("Projection was successful!! Good to go!!!")

    # Polygon boundary selection
    polygonIDFieldName = "STATE_FIPS"
    clipPolygonID = "19"
    arcpy.management.SelectLayerByAttribute(fcPolygon, "NEW_SELECTION", "STATE_FIPS = '19'", None)

    arcpy.CopyFeatures_management(fcPolygon, "NEW_fcPolygon")

    fcClipPolygon = "clipped_polygon"
    arcpy.analysis.Clip("fcLine_Projected", "NEW_fcPolygon", "clipped_Polygon", None)

    # delete extra layer createfrom fcPolygon selection
    arcpy.Delete_management("NEW_fcPolygon")

    # calculate the geometry of clipped polygon
    arcpy.AddGeometryAttributes_management(fcClipPolygon, "LENGTH_GEODESIC", "MILES_US")

    # find total length
    Final_Length = 0

    cursor = arcpy.da.SearchCursor (fcClipPolygon, ["LENGTH_GEO"])
    for row in cursor:
        Final_Length += row[0]

    print(Final_Length)

### def estimateTotalLineLengthInPolygons("north_america_rivers", "clipped_polygon", "STATE_FIPS", "19", "hw5.gdb")

    
#****# I used Near function. So I tweaked the function a little bit. #****#
def countObservationsWithinDistance(fcPoint, search_radius, geodatabase):

    arcpy.env.workspace = geodatabase

    featureclasses = arcpy.ListFeatureClasses()

    # cheking the existance of the feature class in the geodatabase
    if fcPoint in featureclasses:
        print("Featureclass exists in the geodatabase")
    else:
        print("Not in the geodatabase. \n check the data source and set it.")

    # check the shapetype
    des_fcpoint = arcpy.Describe(fcPoint)

    if des_fcpoint.ShapeType == "Point":
        print("Featureclass is a point feature")
    else:
        print("Featureclass maybe either polygon or polyline. Please check again.")

    # checking coordinates
    if des_fcpoint.spatialReference.linearunitName == "":
        print("Warning: ara calculations are not accurate in geographic coordinate systems!")

    # Near analysis
    # Near_FID is the count field
    # set local variables
    in_features = fcPoint
    near_features = fcPoint
    search_radius = "500000 Meters" # you can set your own distance radius
    location = "NO_LOCATION"
    angle = "NO_ANGLE"
    method = "GEODESIC"
    arcpy.analysis.Near(in_features, near_features, search_radius, location, angle, method)
    

### def countObservationsWithinDistance("eu_cities", "500000 Meters", "hw5.gdb")
        
    

    

    

    
    
    
    
