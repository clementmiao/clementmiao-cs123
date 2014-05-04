


def getIdDict():
	id_dict = {}
	player_ids=open("clementmiao-cs123/player_ids.csv","r")
	for line in player_ids.readlines():
		player_list = line.split(",")
		player_id = int(player_list[0])
		player_name = player_list[1] + " " + player_list[2]
		id_dict[player_id] = player_name
	return id_dict



def findPlayerName(player_id,id_dict):
	return id_dict[player_id]