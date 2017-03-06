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
dataDict = {"willBeFuzzy": []}

with open(inputFile + ".csv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    currDivision = None
    currDivDict = None
    for row in fileReader:
        prevDivision = currDivision

        currPlacement = row["placement_type"]
        currDate = row["date"]
        currDepth = row["sample_depth"]
        currDivision = row["division_name"]
        currClass = row["lowest_classification_name"]
        currCount = row["RR_count"]

        # what happens when you get a new division.. lets see, you need to
        # do something with the dictionary you have... you need to append it! here!
        # then
        # create a new dictionary
        # with the "name": = currDivision
        # children = []
        if currDivision != prevDivision:
            if currDivDict != None:
                dataDict["willBeFuzzy"].append(currDivDict)
            currDivDict = {"name": currDivision, "children": []}

        currDivDict["children"].append({"name": currClass, "size": currCount})





#json_string = json.dumps(dataDict, indent=4)
json_string = json.dumps(dataDict, indent=4)
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
