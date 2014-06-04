from py2neo import neo4j,node,rel
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
    pa = '/home/cfisher14/clemetnmiao-cs123'
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
		player_node=batch.create({"name":full_name,"player_id":player_id})
		batch.add_labels(player_node,"player")
		#batch.create(rel(root,"PLAYER",player_node))
		team_node = team_node_dict[team]
		batch.create(rel(player_node,"BELONGS TO",team_node))

	results=batch.submit()


#def process


def 



