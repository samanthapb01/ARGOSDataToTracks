##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2021
## Author: John.Fay@duke.edu (for ENV859)
##---------------------------------------------------------------------

# Import modules
import sys, os, arcpy

#Allow outputs to be overwritten
arcpy.env.overwriteOutput = True

# Set input variables (Hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputSR = arcpy.SpatialReference(54002)
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"

# Create feature class to which we will add features
outPath, outFile = os.path.split(outputFC)
arcpy.management.CreateFeatureclass(outPath,outFile,"POINT","","","",outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class
arcpy.AddField_management(outputFC,"TagID","LONG")
arcpy.AddField_management(outputFC,"LC","TEXT")
arcpy.AddField_management(outputFC,"Date","DATE")

# Create the insert cursor
cur = arcpy.da.InsertCursor(outputFC,['Shape@','TagID','LC','Date'])

#%% Construct a while loop and iterate through all lines in the data file
# Open the ARGOS data file
inputFileObj = open(inputFile,'r')

# Get the first line of data, so we can use the while loop
lineString = inputFileObj.readline()

#Start the while loop
while lineString:
    
    # Set code to run only if the line contains the string "Date: "
    if ("Date :" in lineString):
        
        # Parse the line into a list
        lineData = lineString.split()
        
        # Extract attributes from the datum header line
        tagID = lineData[0]
        
        # Extract location info from the next line
        line2String = inputFileObj.readline()
        
        # Parse the line into a list
        line2Data = line2String.split()
        
        # Extract the date we need to variables
        obsLat = line2Data[2]
        obsLon= line2Data[5]
                    
        # Extract the date, time, and LC values
        obsDate = lineData[3]
        obsTime = lineData[4]
        obsLC   = lineData[7]
        
        # Print results to see how we're doing
        #print (tagID,"Lat:"+obsLat,"Long:"+obsLon, obsLC, obsDate, obsTime)
        
        #Try to convert coordinates to point object
        try:
            # Convert raw coordinate strings to numbers
            if obsLat[-1] == 'N':
                obsLat = float(obsLat[:-1])
            else:
                obsLat = float(obsLat[:-1]) * -1
            if obsLon[-1] == 'E':
                obsLon = float(obsLon[:-1])
            else:
                obsLon = float(obsLon[:-1]) * -1
            
            # Create point object from lat/long coordinates
            obsPoint = arcpy.Point()
            obsPoint.X = obsLon
            obsPoint.Y = obsLat
            
            # Convert the point to a point geometry object with spatial reference
            inputSR = arcpy.SpatialReference(4326)
            obsPointGeom = arcpy.PointGeometry(obsPoint,inputSR)

            # Create a feature object
            feature = cur.insertRow((obsPointGeom,tagID,obsLC,obsDate.replace(".","/") + " " + obsTime))
       
        #Handle any error
        except Exception as e:
            print(f"Error adding record {tagID} to the output: {e}")
        
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
#Close the file object
inputFileObj.close()

#Delete the cursor object
del cur