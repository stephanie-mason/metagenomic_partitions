#==============================================================================#
# This is a simple script to turn some TSV data into JSON for purposes of
# creating a bilevel partition in D3.
#
# Author: Stephanie Mason
#==============================================================================#
import sys, csv, json

#==============================================================================#
# Main Program
#==============================================================================#

# Input Variables
inputFile = sys.argv[1]
highestLevel = sys.argv[2]
# For the future:
# need to add more variables so that there can be as many levels as needed

# Dictionaries
dataDict = {}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        currPlacement = row[highestLevel]
        currDivision = row["division_name"]
        currClass = row["lowest_classification_name"]
        currCount = int(row["RR_count"])

        # Future development: Rather than manually nesting these, need to create
        # some kind of recursive call so that it can work for any number of
        # levels

        # Also update variable names to reflect this...

        if currPlacement not in dataDict:
            dataDict[currPlacement] = {}

        if currDivision not in dataDict[currPlacement]:
            dataDict[currPlacement][currDivision] = {}

        if currClass not in dataDict[currPlacement][currDivision]:
            dataDict[currPlacement][currDivision][currClass] = currCount
        else:
            dataDict[currPlacement][currDivision][currClass] += currCount

# Output dictionaries have a different format
placementFinalDict = {"name": "placements", "children": []}

divIters = 0;
for placement in dataDict:
    # Obviously in the future this will also be recursive so that it can go
    # down as many levels as is needed...
    placementFinalDict["children"].append({"name": placement, "children": []})
    classIters=0
    for division in dataDict[placement]:
        placementFinalDict["children"][divIters]["children"].append({"name": division, "children": []})
        for className in dataDict[placement][division]:
            placementFinalDict["children"][divIters]["children"][classIters]["children"].append({"name": className, "size": dataDict[placement][division][className]})
        classIters += 1
    divIters += 1

# Create the JSON String and write it to file
json_string = json.dumps(placementFinalDict, indent=2)
outputFile = highestLevel + ".json"
outputFile = open(outputFile, 'w')
outputFile.write(json_string)
outputFile.close()
