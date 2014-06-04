import sys
import random
import csv
import numpy


# INITIALIZATION OF CENTROIDS


#Read from the csv and create dictionary. Format: {id:[attributes..]}
def readCSVtoDict(filename):
	pitcher_dict = {}
	csvfile = open(filename,'r')
	reader = csv.reader(csvfile,delimiter=',')
	# row format is id,pitch total,L(bool),R(bool), attributes...
	for row in reader:
		if int(row[1]) != 0:
			pitcher_id = int(row[0])
			atts = row[4:]
			atts = map(lambda x:float(x),atts)
			pitcher_dict[pitcher_id]=atts
	return pitcher_dict


#Write clusters to 'clusters.txt'; csv format, each row represents a cluser
def writeToFile(clusters):
	txtfile = open('clusters_test.txt','w')
	writer = csv.writer(txtfile,delimiter=',')
	for cluster in clusters:
		writer.writerow(cluster)
	txtfile.close()


#Returns euclidean distance between two vectors
def distance(coords1,coords2):
	assert (len(coords1) == len(coords2))
	length = len(coords1)
	sum = 0
	for i in range(length):
		sum += (coords1[i] - coords2[i])**2
	return sum**.5


#Returns distance nearest centroid in centroids_list
def distanceToNearestCentroid(coords,centroid_dict):
	centroids_list = centroid_dict.values()
	min_distance = sys.maxint
	for i in range(len(centroids_list)):
		dist = distance(coords,centroids_list[i])
		if dist < min_distance:
			min_distance=dist
	return min_distance


#zipped should be in this format: [(item,weight),...]
# (Technique found at http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/)
def weightedChoice(zipped):
	totals = []
	running_total = 0
	weights = [x[1] for x in zipped]
	for weight in weights:
		running_total += weight
		totals.append(running_total)

	rnd = random.random() * running_total
	for i in range(len(totals)):
		if rnd < totals[i]:
			return zipped[i][0]


#Initialize centroids using k-means++
def setCentroids(coords_list,k):

	numPitchers = len(coords_list)
	notChosen = range(numPitchers)
	
	centroid_dict={}

	first = random.choice(notChosen)
	centroid_dict[0] = coords_list[first]
	notChosen.remove(first)

	for i in range(1,k):
		weights = []
		
		for n in notChosen:
			dist = distanceToNearestCentroid(coords_list[n],centroid_dict)
			weights.append(dist**2)
		
		zipped = zip(notChosen,weights)
		new_centroid = weightedChoice(zipped)
		centroid_dict[i] = coords_list[new_centroid]
		notChosen.remove(new_centroid)

	return centroid_dict







#THE ACTUAL CLUSTERING


def findNearestCentroid(coords,centroid_dict):
	
	min_distance = sys.maxint
	nearest_centroid = None
	for cluster_num,centroid in centroid_dict.iteritems():
		current_distance = distance(coords,centroid)
		if current_distance < min_distance:
			min_distance = current_distance
			nearest_centroid = cluster_num
	return nearest_centroid







def assignment(pitcher_dict,centroid_dict,k):
	
	next_centroid_dict = {}
	next_cluster_dict = {}
	for i in range(k):
		next_cluster_dict[i] = []


	for pitcher_id, atts in pitcher_dict.iteritems():
		nearest_centroid = findNearestCentroid(atts,centroid_dict)
		next_cluster_dict[nearest_centroid].append(pitcher_id)


	for cluster_num,pitchers in next_cluster_dict.iteritems():

		clustersum = numpy.array([0] * (12*11))

		for pitcher in pitchers:
			atts = pitcher_dict[pitcher]
			clustersum += numpy.array(atts)
		print pitchers
		centroid = list(clustersum/len(pitchers))
		next_centroid_dict[cluster_num] = centroid
	return (next_centroid_dict,next_cluster_dict)






def main(argv):

	pitcher_dict = readCSVtoDict("results_aggregation.txt")

	k = int(argv[0])
	#Hardcoding k = 20 for now.
	centroid_dict = setCentroids(pitcher_dict.values(),k)
	
	stop = False

	cluster_dict = {}
	reps = 0
	while not stop and reps < 1000:

		next = assignment(pitcher_dict,centroid_dict,k)

		if cluster_dict == next[1]:
			stop = True
		else: 
			centroid_dict = next[0]
			cluster_dict = next[1]
			reps += 1

	writeToFile(cluster_dict.values())





main(sys.argv[1:])



