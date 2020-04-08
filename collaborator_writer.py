# this code reads the "performers" data set and writes
# a csv which contains only only_collaborators.

import csv

collaborators = []

# create a list which considers only musicians who collaborate
with open('performers.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    index = 0
    for row in spamreader:
        # fetch the performer string we are going to look at
        s = row[index]
        # find '&' symbol (don't worry about how many yet)
        if " & " in s:
            # uniqueness modifier
            if s not in collaborators:
                collaborators.append(s)



collaborators.sort()

with open('only_collaborators_raw.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n')
    spamwriter.writerow(collaborators)
