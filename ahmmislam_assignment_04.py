# Assignment 04/Author
def hawkid():
    return(["A H M Mainul Islam", "ahmmislam"])

# Import system moduels
import arcpy
import os

### Task 01 Function
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):

    try:
        # Set workspace environment
        arcpy.env.workspace = input_geodatabase
        arcpy.outputOverwrite = True

        # find the nearest polyline from each points
        arcpy.Near_analysis(fcPoint, fcPolyline)

        # set local variables
        field_name = "DIS_TO_POLYLINE"
        field_type = "DOUBLE"

        # execute add field for point feature class
        arcpy.management.AddField(fcPoint, field_name, field_type)

        # update the newly added field using update cursor
        with arcpy.da.UpdateCursor (fcPoint, ["NEAR_DIST", field_name]) as cursor:
            for row in cursor:
                row[1]=row[0]
                cursor.updateRow(row)
                
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())

### Task 02 Function
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):

    try:
        # set workspace environment
        arcpy.env.workspace = input_geodatabase
        arcpy.outputOverwrite = True

        # set local variables to use in creating new layer
        NewpointLayer = "pnt_layer_selection"

        # make new layer
        arcpy.MakeFeatureLayer_management(fcPoint, NewpointLayer)

        # set local variables to select specific attributes
        pointFieldName = "FACILITY"
        pointFieldValue = "HEALTH CENTER"
        condition = "pointFieldName = 'pointFieldValue'"

        # output will be selected attributes based on the applied condition
        arcpy.SelectLayerByAttribute_management(NewpointLayer, "NEW_SELECTION", condition)

        # set local variables for applying spatial join
        output_layer = "Join_output"
        join_operation = "JOIN_ONE_TO_ONE"
        join_type = "KEEP_ALL"
        match_option = "COMPLETELY_CONTAINS"

        # output will be a new layer with JOIN_COUNT
        arcpy.SpatialJoin_analysis(fcPolygon, fcpointLayer, output_layer, join_operation, join_type, match_option)
        
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())

### Task 03 Function
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, pointFieldValue fcPolygon, workspace):

    try:
        # set workspace environment
        arcpy.env.workspace = workspace
        arcpy.outputOverwrite = True

        # set local variables 
        fcPoint = "facilities"
        pointFieldName = "FACILITY"

        # creating a list of pointFieldName field values
        with arcpy.da.SearchCursor(fcPoint, pointFieldName) as cursor:
            myValues = sorted({row[0] for row in cursor})

        # remove the white space and limiting the characters of the field values within 13
        # add the values in the polygon feature class
        for field in myValues:
            emptyField = field.replace(" ", "").strip()[0:13]
            arcpy.management.AddField(fcPolygon, emptyField, "LONG")

        # set local variable to create a new layer
        NewpointLayer = "fc_point_layer"

        # output will be a new layer
        arcpy.MakeFeatureLayer_management(fcPoint, NewpointLayer)

        # set parameters for selecting the attributes
        pointFieldName = "FACILITY"
        pointFieldValue = "HEALTH CENTER"
        condition = "pointFieldName = 'pointFieldValue'"

        # output will be selected attributes based on the condition
        arcpy.SelectLayerByAttribute_management(NewpointLayer, "NEW_SELECTION", condition)

        # set local variables for applying spatial join
        output_layer = "join_output"
        join_operation = "JOIN_ONE_TO_ONE"
        join_type = "KEEP_ALL"
        match_option = "COMPLETELY_CONTAINS"

        # output will be a new join layer with JOIN_COUNT
        arcpy.SpatialJoin_analysis(fcPolygon, NewpointLayer, output_layer, join_operation, join_type, match_option)

        # calculate field for specific point field types
        input_table = output_layer
        Field_Name = "HEALTHCENTER" ##### any sorted field names from myValues can be used here
        arcpy.management.CalculateField(output_layer, Field_Name, "!Join_Count!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())


     

