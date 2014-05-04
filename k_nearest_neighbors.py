import numpy
from heapq import heappush,heappop 




#Computes distance squared given two points (lists of coordinates)
def findDistance(a_coordinates,b_coordinates):
	sum = 0
	for tuple in zip(a_coordinates,b_coordinates):
		sum += (tuple[0] - tuple[1]) * (tuple[0] - tuple[1])
	return sum



#Finds k nearest neighbors of pitcher from pitcher_list
#Expected format: (pitcher_id,[coordinates])

def findkNearest(k,pitcher,pitcher_list):
	nearest_points = []
	for x in pitcher_list:
		pitcher_id = x[0]
		distance = findDistance(pitcher[1],x[1])
		if len(nearest_points) == k:
			#heapq apparently does not have max-heaps, hence negative distance.
			heappush(nearest_points,(-distance,pitcher_id))
			heappop(nearest_points)
		else:
			heappush(nearest_points,(-distance,pitcher_id))
	nearest_pitcher_ids = []
	while len(nearest_points) != 0:
		nearest_pitcher_ids.append(heappop(nearest_points)[1])
	return nearest_pitcher_ids
