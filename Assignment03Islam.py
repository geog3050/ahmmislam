###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["A H M Mainul Islam", "ahmmislam"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 


def printFeatureClassNames(workspace):
    # import system module 
    import arcpy
    import os

    # Set environment settings
    arcpy.env.workspace = "hw3.gdb"
    arcpy.env.overwriteOutput = True
    featureclasses = arcpy.ListFeatureClasses()

    for fc in featureclasses:
        print(fc)

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    import arcpy
    import os

    #featureclasses = arcpy.ListFeatureClasses()

    #for fc in featureclasses:
        #print(fc)

    for field in arcpy.ListFields(inputFc, field_type= "Integer" and "Double" and "Float"):
##        if field.type in ("Double", "Integer", "Float"):
            print(field.name, field.type)
    

    

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):

    import arcpy
    import os
    
    arcpy.env.workspace = input_geodatabase
    try:
        arcpy.CreateFileGDB_management(output_geodatabase)
    except:
        print("The error with output geodatabase name")
    try:
        featureclasses = arcpy.ListFeatureClasses()
        out_workspace = output_geodatabase
    
        for fc in featureclasses:
            descObject = arcpy.Describe(fc)
            if descObject.shapeType == shapeType:
                out_featureclass = os.path.join(out_workspace, os.path.splitext(fc)[0])
    
                arcpy.CopyFeatures_management(fc, out_featureclass)
            
    except:
        print("Errors with featureclasses")
        
    return
    

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    pass


######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
