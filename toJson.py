#==============================================================================#
# This is a simple script to turn some TSV data into JSON for purposes of
# creating a bilevel partition in D3.

# The intended use is with an input file contains 18s data with
# columns for the division name and the lowest classification name, with
# RR counts for the lowest classifications.
# The JSON output has the confidence level as the root, with division names
# as the next level and lowest classifications & their counts as the leaves
#
# However, it can be used in a general case with any single level parent/child
# relationship given counts on the children.
#
# Output is a json file with the same name as the tsv input file
#
# Author: Stephanie Mason
#==============================================================================#
import sys, csv

#==============================================================================#
# Main Program
#==============================================================================#

if len(sys.argv) != 6:
    print("Usage: toJson.py file_name parent_col child_col child_count_col")
    sys.exit()

# Input Variables
inputFile = sys.argv[1]
categoryCol = sys.argv[2]
parentCol = sys.argv[3]
childCol = sys.argv[4]
childCountCol = sys.argv[5]

# Output Variables
outputFile = inputFile + ".json"
outputFile = open(outputFile, 'w')

# Let the user know what the args were
print(inputFile + ", " + parentCol + ", " + childCol + ", " + childCountCol)

# Write the JSON file
outputFile.write("{ \r\n")

currParent = None
firstRun = True
firstChild = True
limitRows = 0;
with open(inputFile + ".tsv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
        if firstRun:
            outputFile.write("\t\"name\": \"" + row[categoryCol] + "\",\r\n")
            outputFile.write("\t\"children\": [\r\n" )
            outputFile.write("\t{\r\n")
        lastParent = currParent
        currParent = row[parentCol]
        if limitRows < 80:

            if currParent != lastParent:
                if firstRun != True:
                    outputFile.write("\r\n\t\t] \r\n\t }, \r\n\t { \r\n")
                outputFile.write("\t\t\"name\": \"" + row[parentCol] + "\",\r\n")
                outputFile.write("\t\t\"children\": [\r\n" )
                lastParent = currParent
                firstChild = True
            if currParent == lastParent:
                if firstChild != True:
                    outputFile.write(",\r\n")
                outputFile.write("\t\t\t{\"name\": \"" + row[childCol] + "\", \"size\": " + row[childCountCol] + "}")
        limitRows += 1
        firstRun = False
        firstChild = False

outputFile.write("\t\t]\r\n \t}\r\n \t]\r\n }")



#==============================================================================#
# Function Definitions
#==============================================================================#

outputFile.close()
