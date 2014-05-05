import numpy
from heapq import heappush,heappop 
import pickle

#reads player_ids.csv into a dictionary
def getIdDict():
	id_dict = {}
	player_ids=open("player_ids.csv","r")
	for line in player_ids.readlines():
		player_list = line.split(",")
		player_id = player_list[0]
		player_name = player_list[1] + " " + player_list[2]
		id_dict[player_id] = player_name
	return id_dict


# Returns player's name
def findPlayerName(player_id,id_dict):
	if player_id in id_dict.keys():
		return id_dict[player_id]
	else:
		return "Player Id # not found in player_ids.csv"
		
		
#Computes distance squared given two points (lists of coordinates)
def findDistance(a_coordinates,b_coordinates):
	sum = 0
	for tuple in zip(a_coordinates,b_coordinates):
		sum += (tuple[0] - tuple[1]) * (tuple[0] - tuple[1])
	return sum



#Finds k nearest neighbors of pitcher from pitcher_list
#Expected format: (pitcher_id,[coordinates])

def findkNearest(k,pitcher,pitcher_list):

	attributes_list = ['@break_angle', '@break_length', '@break_y', '@pfx_x', '@pfx_z', '@spin_dir', '@spin_rate', '@start_speed', '@x0', '@y0', '@z0']
	pitch_type_list = ['FF','FT','FC','SI','SF','SL','CH','CB','KC','KN','EP']
	pitcher_a_coordinates = []
	for pitch in pitch_type_list:
		for attribute in attributes_list:
			pitcher_a_coordinates.append(pitcher[1][pitch][attribute])

	nearest_points = []
	for x in pitcher_list:
		pitcher_id = x[0]
		pitcher_b_coordinates = []
		for pitch in pitch_type_list:
			for attribute in attributes_list:
				pitcher_b_coordinates.append(x[1][pitch][attribute])

		distance = findDistance(pitcher_a_coordinates,pitcher_b_coordinates)
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
	
	
	

def mainFunction():
	print "Test case: find 15 most similar pitchers to Max Scherzer."


	results = open("results.p","r")
	pitcher_list = pickle.load(results)
	scherzer_id = '453286'
	scherzer_index = -1
	i = 0
	for pitcher in pitcher_list:
		if pitcher[0] == scherzer_id: 
			scherzer_index = i
		else: 
			i = i + 1

	assert scherzer_index != -1, "Pitcher not found"
	scherzer_like = findkNearest(15, pitcher_list[i], pitcher_list)
	print scherzer_like
	id_dict = getIdDict()
	for pitcher in scherzer_like:
		print pitcher + ": " + findPlayerName(pitcher,id_dict)
	
	
	
mainFunction()
	

