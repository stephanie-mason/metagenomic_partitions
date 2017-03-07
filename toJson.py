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
hierarchyType = sys.argv[2]

# Dictionaries
dataDict = {}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        currPlacement = row["placement_type"]
        #currDate = row["date"]
        #currDepth = row["sample_depth"]
        currDivision = row["division_name"]
        currClass = row["lowest_classification_name"]
        currCount = int(row["RR_count"])

        if currPlacement not in dataDict:
            dataDict[currPlacement] = {}

        if currDivision not in dataDict[currPlacement]:
            dataDict[currPlacement][currDivision] = {}

        if currClass not in dataDict[currPlacement][currDivision]:
            dataDict[currPlacement][currDivision][currClass] = currCount
        else:
            dataDict[currPlacement][currDivision][currClass] += currCount

print(dataDict["fuzzy"]["Alveolata"]["Dinophyceae"])

json_string = json.dumps(dataDict, indent=2)
outputFile = "all_data.json"
outputFile = open(outputFile, 'w')
outputFile.write(json_string)
outputFile.close()

# Write output dictionaries
placementFinalDict = {"name": "placements", "children": []}

divIters = 0;
for placement in dataDict:
    placementFinalDict["children"].append({"name": placement, "children": []})
    classIters=0
    for division in dataDict[placement]:
        placementFinalDict["children"][divIters]["children"].append({"name": division, "children": []})
        for className in dataDict[placement][division]:
            placementFinalDict["children"][divIters]["children"][classIters]["children"].append({"name": className, "size": dataDict[placement][division][className]})
        classIters += 1
    divIters += 1

finalDict = placementFinalDict

json_string = json.dumps(finalDict, indent=2)
#print(json_string)

# Outputs
outputFiles = ["placement_sorted.json", "date_sorted.json", "depth_sorted.json"]

for outputFile in outputFiles:
    outputFile = open(outputFile, 'w')
    outputFile.write(json_string)
    outputFile.close()
