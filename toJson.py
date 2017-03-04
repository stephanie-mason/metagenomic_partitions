#==============================================================================#
# This is a simple script to turn some TSV data into JSON for purposes of
# creating a bilevel partition in D3.

# The intended use is with an input file contains 18s data with
# columns for the division name and the lowest classification name, with
# RR counts for the lowest classifications.
# The JSON output has the lowest classification names and the counts
# as children of the division name.
#
# However, it can be used in a general case with any single level parent/child
# relationship given counts on the children.
#
# Output is a JSON file with the same name as the tsv input file
#
# Author: Stephanie Mason
#==============================================================================#
import sys, csv

#==============================================================================#
# Main Program
#==============================================================================#

if len(sys.argv) != 5:
    print("Usage: toJson.py file_name parent_col child_col child_count_col")
    sys.exit()

inputFile = sys.argv[1]
parentCol = sys.argv[2]
childCol = sys.argv[3]
childCountCol = sys.argv[4]

outputFile = inputFile + ".json"
outputFile = open(outputFile, 'w')


print(inputFile + ", " + parentCol + ", " + childCol + ", " + childCountCol)

with open(inputFile + ".tsv", newline='') as tsvFile:
    fileReader = csv.DictReader(tsvFile, delimiter='\t')
    for row in fileReader:
            outputFile.write(row[parentCol] + " " + row[childCol])


#==============================================================================#
# Function Definitions
#==============================================================================#

outputFile.close()
