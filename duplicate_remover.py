# removes duplicates from a csv.

import csv

uniqueOnly = []

# create a list which considers only musicians who collaborate
with open('only_collaborators_formatted.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    index = 0
    for row in spamreader:
        # fetch the performer string we are going to look at
        s = row[index]
        # uniqueness modifier
        if s not in uniqueOnly:
            uniqueOnly.append(s)




uniqueOnly.sort()

with open('only_collaborators_unique.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n')
    spamwriter.writerow(uniqueOnly)
