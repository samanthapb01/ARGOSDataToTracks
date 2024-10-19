##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2024
## Author: slp87@duke.edu (for ENV859)
##---------------------------------------------------------------------

#Import Packages
import sys, os, arcpy

#Set input variable (hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997g.txt'
outputFC = 'V:/ARGOSTracking/Scratch/ARGOSTrack.shp'
