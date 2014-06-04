from py2neo import neo4j,node,rel,cypher
import os
import sys
import glob
import subprocess
import json
#import numpy as np
import xml.etree.ElementTree as ET
#from sets import Set


def playerTeam():
    d = {}
    for root, dirs, filenames in os.walk('players_07'):
        for f in filenames:
            path = os.path.join('players_07', f)
            tree = ET.parse(path)
            game = tree.getroot()
            for team in game:
                if(team.tag != 'umpires'):
                    name = team.get('name')
                    #print("name: " + name)
                    for player in team:
                        pid = player.get('id')
                        last = player.get('last')
                        first = player.get('first')
                        #print("ID: " + pid)
                        d[pid] = (name, first + " " + last)
    #for p in d:
    #    print("This should work " + p + " " + d[p][0] + " " + d[p][1])
    return d        


def processPlayerTeam(playerteam_dict,graph_db,root):
	teams = set({})
	# Add teams to database, connected to root node
	# (Currently, each team requires a separate HTTP request)
	team_node_dict = {}
	for pair in playerteam_dict.values():
		team = pair[0]
		teams.add(team)
	for team in teams:
		team_node,relation = graph_db.create({"name":team},rel(root,"TEAM",0))
		team_node.add_labels("team")
		team_node_dict[team] = team_node

	#Add players to database as a batch
	batch = neo4j.WriteBatch(graph_db)
	for player_id, player_tuple in playerteam_dict.iteritems():
		team = player_tuple[0]
		full_name = player_tuple[1]
		player_node=batch.create({"name":full_name,"player_id":int(player_id)})
		batch.create(rel(root,"PLAYER",player_node))
		batch.add_labels(player_node,"player")
		team_node = team_node_dict[team]
		batch.create(rel(player_node,"PLAYS FOR",team_node))

	results=batch.submit()



def readClustersToDict(clusters_file):
	f = open(clusters_file,'r')
	cluster_number = 1

	#Format: {clusternum:[id1,id2,..],..}
	cluster_dict = {}
	for line in f.readlines():
		pitcher_ids = line.split(',')
		cluster_dict[cluster_number] = pitcher_ids
		cluster_number += 1

	return cluster_dict



def processClusters(cluster_dict,graph_db,root):

	for cluster_number in cluster_dict:
		batch = neo4j.WriteBatch(graph_db)
		name = "Cluster " + str(cluster_number)
		cluster_node = batch.create({"name":name,"cluster_number":cluster_number})
		batch.create(rel(root,"CLUSTER",cluster_node))
		batch.add_labels(cluster_node,"cluster")
		for pitcher_id in cluster_dict[cluster_number]:
			for player_node in graph_db.find("player",property_key="player_id",property_value=int(pitcher_id)):
				batch.create(rel(player_node, "BELONGS TO",cluster_node))
		
		batch.submit()



def readMatchupsToDict(matchups_file):
	f = open(matchups_file,'r')

	matchups_dict = {}
	for line in f.readlines():
		line = line.split('\t')
		player_id = int(line[0])
		matchups = line[1].split(',')[1:]
		matchups = map(lambda x: float(x),matchups)
		num_clusters = len(matchups)/2
		player_matchups=[]
		for i in range(num_clusters):
			player_matchups.append([matchups[0],matchups[1]])
			matchups = matchups[2:]
		matchups_dict[player_id]=player_matchups
	return matchups_dict

def processMatchups(matchups_dict,graph_db):
	
	for player_id in matchups_dict:
		batch = neo4j.WriteBatch(graph_db)
		for player_node in graph_db.find("player",property_key="player_id",property_value=player_id):
			for cluster_node in graph_db.find("cluster"):
				cluster_number = cluster_node['cluster_number']
				cluster_matchup = matchups_dict[player_id][cluster_number-1]
				plate_appereances= cluster_matchup[1]
				if (plate_appereances == 0): on_base_percentage = 0.0
				else: on_base_percentage = round(cluster_matchup[0]/plate_appereances,3)
				batch.create(rel(player_node,"MATCHUP",cluster_node, \
					{"OBP":on_base_percentage,"PA":plate_appereances}))
		batch.submit()


def populateGraphDB(playerteam_dict,cluster_dict,matchups_dict,graph_db):

	graph_db.clear()

	root = graph_db.get_or_create_indexed_node("root","k1","v1")

	processPlayerTeam(playerteam_dict,graph_db,root)

	processClusters(cluster_dict,graph_db,root)

	processMatchups(matchups_dict,graph_db)





def main():
	playerteam_dict = playerTeam()
	cluster_dict = readClustersToDict("clusters.txt")
	matchups_dict = readMatchupsToDict("results_matchups.txt")
	graph_db = neo4j.GraphDatabaseService()

	populateGraphDB(playerteam_dict,cluster_dict,matchups_dict,graph_db)



def recommendHitters(pitcher_name,hitting_team):
	query = "MATCH (p:player)-[:`BELONGS TO`]-(c:cluster)-[m:`MATCHUP`]-\
	(b:player)-[:`PLAYS FOR`]-(t:team) WHERE p.name = '" + pitcher_name +  \
	"' and t.name ='"+ hitting_team + "' and m.PA > 0 RETURN b.name,m.OBP,m.PA ORDER BY m.OBP DESC;"

	session = cypher.Session()

	tx = session.create_transaction()

	tx.append(query)

	response = tx.commit()

	response = response[0]

	for hitter in response:
		data = hitter.values
		print data[0] + "  OBP: " + str(data[1]) + "  PA: " + str(data[2])



def recommendPitchers(batter_name,pitching_team):
	query = "MATCH (b:player)-[m:MATCHUP]-(c:cluster)-[:`BELONGS TO`]-\
	(p:player)-[:`PLAYS FOR`]-(t:team) WHERE t.name = '"+ pitching_team+ "'\
	 and b.name = '"+ batter_name+"' RETURN p.name,m.OBP,m.PA ORDER BY m.OBP;"

	session = cypher.Session()

	tx = session.create_transaction()

	tx.append(query)

	response = tx.commit()

	response = response[0]

	for pitcher in response:
		data = pitcher.values
		print data[0] + "  OBP: " + str(data[1]) + "  PA: " + str(data[2])


if (sys.argv[1] == "main"):
	main()
elif (len(sys.argv) == 4 and sys.argv[1] == "pitcher"):
	recommendPitchers(sys.argv[2], sys.argv[3])
elif (lens(sys.argv) == 4 and sys.argv[1] == "hitter"):
	recommendHitters(sys.argv[2], sys.argv[3])
else:
	print "Format is [main/pitcher/hitter] [ /batter_name/pitcher_name] [ /your_team]"





