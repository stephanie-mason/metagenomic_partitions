#==============================================================================#
# This is a simple script to turn some TSV data into JSON for purposes of
# creating a bilevel partition in D3.
#
# It writes a JSON file with a hierarchy given in the arguments
#
# IE Arg1 will have children Arg2, which will have children Arg 3
#
# Output is a json file with the same name as the input file
#
# Author: Stephanie Mason
#==============================================================================#
import sys, csv, json

#==============================================================================#
# Main Program
#==============================================================================#

# Input Variables
inputFile = sys.argv[1]

# Output Variables
outputFile = inputFile + ".json"
outputFile = open(outputFile, 'w')

# Nested Dictionaries
dataDict = {}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        currPlacementType = row["placement_type"]
        currDate = row["date"]
        dataDict[currPlacementType] = currDate

print(dataDict)

outputFile.close()
