import csv

collaborators = []

# create a list which considers only musicians who collaborate
with open('performers.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    index = 0
    for row in spamreader:
        s = row[index]
        # find & symbol (don't worry about how many yet)
        if " & " in s:
            # uniqueness modifier
            if s not in collaborators:
                collaborators.append(s)

# remove clones.


collaborators.sort()

with open('performers_who_collaborate.csv', 'w', newline='\n') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\n')
    spamwriter.writerow(collaborators)
