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
dataDict = {"name": "dates", "children": []}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    currPlacement = None
    currDate = None
    currDepth = None
    currDivision = None

    currPlaceDict = None
    currDateDict = None
    currDepthDict = None
    currDivDict = None
    for row in fileReader:
        prevPlacement = currPlacement
        prevDate = currDate
        prevDepth = currDepth
        prevDivision = currDivision

        currPlacement = row["placement_type"]
        currDate = row["date"]
        currDepth = row["sample_depth"]
        currDivision = row["division_name"]
        currClass = row["lowest_classification_name"]
        currCount = row["RR_count"]

        # New Placement Type
        #if currPlacement != prevPlacement:
        #    currPlaceDict = {"name": currPlacement, "children": []}
        #    dataDict["children"].append(currPlaceDict)

        # New Date
        if currDate != prevDate:
            currDateDict = {"name": currDate, "children": []}
            dataDict["children"].append(currDateDict)

        # New depth in Date

        # New Division
        if currDivision != prevDivision:
            if currDivDict != None:
                currDateDict["children"].append(currDivDict)
            currDivDict = {"name": currDivision, "children": []}

        currDivDict["children"].append({"name": currClass, "size": currCount})





json_string = json.dumps(dataDict, indent=2)
print(json_string)
outputFile.write(json_string)

outputFile.close()

# Key                           # value(s)
# confidence level              date dictionary
# date                          sample_depth dictionary
# sample depth                  division dictionary
# division                      name, lowest classification dictionary
# lowest classification         name of gene, size

#row["sample_depth"]} for row in fileReader
