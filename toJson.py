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

# New tactic: First build a set of dictionaries from the data,
# iterating through it once
# One for Date, one for Depth, one for Placement Type
# This dictionary will have the keys that are values from the table
# THEN !!!!
# Make new output dictionaries that have "name" keys and list values from
# your handy, descriptive key dictionaries
# Dictionaries everywhere!!!

# Dictionaries
# First Level Dicts
placementDict = {}
dateDict = {}
depthDict = {}

# Second Level Dict
#divisionDict = {}

# Third Level Dict
#classDict = {}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        currPlacement = row["placement_type"]
        #currDate = row["date"]
        #currDepth = row["sample_depth"]
        currDivision = row["division_name"]
        currClass = row["lowest_classification_name"]
        currCount = int(row["RR_count"])

        if currPlacement not in placementDict:
            placementDict[currPlacement] = {}

        if currDivision not in placementDict[currPlacement]:
            placementDict[currPlacement][currDivision] = {}

        if currClass not in placementDict[currPlacement][currDivision]:
            placementDict[currPlacement][currDivision][currClass] = currCount
        else:
            placementDict[currPlacement][currDivision][currClass] += currCount

        #placementDict[currPlacement] = divisionDict
        #divisionDict[currDivision] = classDict

        #if currClass in classDict:
        #    placementDict[currPlacement][currDivision][currClass] += currCount
        #else:
        #    placementDict[currPlacement][currDivision][currClass] = currCount


print(placementDict["fuzzy"]["Alveolata"]["Dinophyceae"])

json_string = json.dumps(placementDict, indent=2)
outputFile = "all_data.json"
outputFile = open(outputFile, 'w')
outputFile.write(json_string)
outputFile.close()

# Write output dictionaries
placementFinalDict = {"name": "placements", "children": []}

iters = 0;
for placement in placementDict:
    placementFinalDict["children"].append({"name": placement, "children": []})
    for division in placementDict[placement]:
        inneriters=0
        placementFinalDict["children"][iters]["children"].append({"name": division, "children": []})
        for className in placementDict[placement][division]:
            placementFinalDict["children"][iters]["children"][inneriters]["children"].append({"name": className, "size": placementDict[placement][division][className]})
        inneriters += 1
    iters += 1

finalDict = placementFinalDict

json_string = json.dumps(finalDict, indent=2)
#print(json_string)

# Outputs
outputFiles = ["placement_sorted.json", "date_sorted.json", "depth_sorted.json"]

for outputFile in outputFiles:
    outputFile = open(outputFile, 'w')
    outputFile.write(json_string)
    outputFile.close()
