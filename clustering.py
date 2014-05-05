import numpy
from heapq import heappush,heappop 






#reads player_ids.csv into a dictionary
def getIdDict():
	id_dict = {}
	player_ids=open("player_ids.csv","r")
	for line in player_ids.readlines():
		player_list = line.split(",")
		player_id = int(player_list[0])
		player_name = player_list[1] + " " + player_list[2]
		id_dict[player_id] = player_name
	return id_dict


# Returns player's name
def findPlayerName(player_id,id_dict):
	if player_id in id_dict.keys():
		return id_dict[player_id]
	else:
		print "Error: Id # not found"
		exit()
		
		
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
