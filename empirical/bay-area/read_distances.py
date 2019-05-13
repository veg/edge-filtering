import csv
import scipy.stats

distances = list(csv.reader(open('../lanl/results/raw_reference.fas_user.tn93output.csv', newline=''), delimiter=',', quotechar='|'))

# Get distribution of distances via histogram
distances = [float(x[2]) for x in distances[1:]]
print(scipy.stats.beta.fit(distances))

