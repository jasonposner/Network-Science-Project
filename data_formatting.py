import csv

performers = []

# only fetch the artists
with open('hot_stuff.csv', newline='\n') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
         performers.append(row[4])

performers.sort()

print(performers)
