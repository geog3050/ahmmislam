# Author: A H M Mainul Islam
# Final Project
# Investigating the impact of Hurricane Irma on Everglades National Park
# Importing the system module
import arcpy

import os

import arcgis
from datetime import date

# setting the workspace
arcpy.env.workspace = "DataNew"
arcpy.overwriteOutput = True

# calling the raster files from the folder and calculating rasters
# NDVI is an idex to determine the greenness of a plant or vegetation
# NDVI = (NIR-RED)/(NIR+RED)
# NIR band of RapidEye is 5 and RED band is 3
# Need to do it for all the reference period rasters from the folder (2015-2017)
NDVI_raster = arcpy.ia.NDVI("2020_01_Harney_River.tif", 5, 3)

# Saving the outputs with work day specific name
today = date.today()
date = today.strftime("%d-%m-%Y")
NDVI_raster.save("DataNew"+'\\'+date+'_' +'NDVI_2015.tif') # change the name as per the year. For example, NDVI_2016, NDVI_2017

# calculating the mean of reference period
Mean_raster = arcpy.ia.CellStatistics("30-04-2022_NDVI_2015.tif;30-04-2022_NDVI_2016.tif;30-04-2022_NDVI_2017.tif", "MEAN", "DATA", "SINGLE_BAND", 90, "AUTO_DETECT")

# saving the raster file
Mean_raster.save("Mean_RefPeriod.tif")

# check the coordinate system
check_Coordinate_raster = arcpy.Describe("Mean_RefPeriod.tif").spatialReference.Name
check_Coordinate_raster

check_Coordinate_layer = arcpy.Describe("LandArea_Region3&4").spatialReference.Name
check_Coordinate_layer

ProjectedSHP = "fcShp_PRJN"

if check_Coordinate_layer is not check_Coordinate_raster:
    print ("The coordinate systems are not same. One of them need to be projected as per another one.")
    arcpy.Project_management("LandArea_Region3&4", ProjectedSHP, arcpy.Describe("Mean_RefPeriod.tif").spatialReference)

# importing system for using raster calculations
from arcpy.sa import *

# masking out the water from the raster
mean_raster_masked = arcpy.sa.ExtractByMask("Mean_RefPeriod.tif", "fcShp_PRJN")

# NDVI change calculation for 2018, 2019, 2020
# NDVI change calculation for 2018
# change of NDVI = NDVI mean of reference period - NDVI of specific year image
outMinus = Minus("Mean_RefPeriod.tif", "30-04-2022_NDVI_2018.tif")
outMinus.save("Datanew/Change_2018.tif")
out_raster18 = arcpy.sa.ExtractByMask("Change_2018.tif", ProjectedSHP)
out_raster18.save("chng2018.tif")

# NDVI change calculation for 2019
outMinus19 = Minus("Mean_RefPeriod.tif", "30-04-2022_NDVI_2019.tif")
outMinus19.save("Change_2019.tif")
out_raster19 = arcpy.sa.ExtractByMask("Change_2019.tif", ProjectedSHP)
out_raster19.save("chng2019.tif")

# NDVI change calculation for 2020
outMinus20 = Minus("DataNew/Mean_RefPeriod.tif", "30-04-2022_NDVI_2020.tif")
outMinus20.save("Datanew/Change_2020.tif")
out_raster20 = arcpy.sa.ExtractByMask("Change_2020.tif", ProjectedSHP)
out_raster20.save("chng2020.tif")

# Reclassify the raster of 2018 to check the negative and positive change
reclass_raster18 = arcpy.sa.Reclassify("chng2018.tif", "VALUE", "-0.562587 0 1;0 1 2", "DATA")
reclass_raster18.save("Reclass_2018.tif")

# Reclassify the raster of 2019 to check the negative and positive change
reclass_raster19 = arcpy.sa.Reclassify("chng2019.tif", "VALUE", "-0.745011 0 1;0 1 2", "DATA")
reclass_raster19.save("Reclass_2019.tif")

# Reclassify the raster of 2020 to check the negative and positive change
reclass_raster20 = arcpy.sa.Reclassify("chng2020.tif", "VALUE", "-0.908696 0 1;0 1 2", "DATA")
reclass_raster20.save("Reclass_2020.tif")


# Calculating mean for the post-hurricane NDVI change rasters
Mean_Sev_raster = arcpy.ia.CellStatistics("chng2018.tif;chng2019.tif;chng2020.tif", "MEAN", "DATA", "SINGLE_BAND", 90, "AUTO_DETECT")


# Seerity calculation
# categories are based on deviations from the mean of reference period
# -1 to -0.54= High
# -0.54 to -0.14 = Moderate
# -0.14 to 0.26 = Low
# 0.26 to 0.66 = Neutral
# 0.66 to 1 = Positive
sev_raster18_new = arcpy.sa.Reclassify("chng2018.tif", "VALUE", "-1 -0.54 1;-0.54 -0.14 2;-0.14 0.26 3;0.26 0.66 4;0.66 1 5", "DATA")
sev_raster19_new = arcpy.sa.Reclassify("chng2019.tif", "VALUE", "-1 -0.54 1;-0.54 -0.14 2;-0.14 0.26 3;0.26 0.66 4;0.66 1 5", "DATA")
sev_raster20_new = arcpy.sa.Reclassify("chng2020.tif", "VALUE", "-1 -0.54 1;-0.54 -0.14 2;-0.14 0.26 3;0.26 0.66 4;0.66 1 5", "DATA")


