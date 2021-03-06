import os, json
import numpy as np
import pickle



def get_data(file_name):
    f = open(file_name, "r+")   
    data = json.load(f)4
    f.close()
    return data

def produce_results(dic, file_name):
    #desired attributes: pitch type, handedness, break_angle, break_length, break_y, pfx_x, pfx_z, spin_dir, spin_rate, start_speed, x0, y0, z0
    #structure of each pitcher: tuple (pitcher_id, [vector of attributes])
    data = get_data(file_name)['game']
    inning = data['inning']
    if isinstance(inning, dict):
        inning = [inning]
    for inn in inning:
        tb = []
        if 'top' in inn.keys():
            top = inn['top']
            tb.append(top)
        if 'bottom' in inn.keys():
            bottom = inn['bottom']
            tb.append(bottom)
        for x in tb:
            if x != None:
                if 'atbat' in x.keys():
                    l = x['atbat']
                    if isinstance(l, dict):
                        l = [l] 
                    for m in l:
                        #start pitch type
                        pitcher = m['@pitcher']
                        if 'pitch' in m.keys():
                            pitch = m['pitch']
                            pitch_possibilities = [['FF','FA'],['FT'],['FC'],['SI','FS'],['SF'],['SL'],['CH'],['CB','CU'],['KC'],['KN'],['EP']]
                            attributes_list = ['@break_angle', '@break_length', '@break_y', '@pfx_x', '@pfx_z', '@spin_dir', '@spin_rate', '@start_speed', '@x0', '@y0', '@z0']
                            #end pitch type
                            if pitcher not in dic:
                                dic[pitcher] = {}
                                #start left handed or right handed
                                dic[pitcher]['handedness'] = m['@p_throws']
                                #end left handed or right handed
                                for poss in pitch_possibilities:
                                    dic[pitcher][poss[0]] = {}
                                    pitch_dic = dic[pitcher][poss[0]]
                                    pitch_dic['counter'] = 0.0
                                    for att in attributes_list:
                                        pitch_dic[att] = 0.0

                                    # pitch_type[poss[0]] = 0
                                dic[pitcher]['total'] = 0.0
                                #end pitch type
                            if isinstance(pitch, dict): #this is because if there is only one throw, then the data is in a dictionary instead of a list of dictionaries
                                pitch = [pitch]
                            for pi in pitch:
                                #start pitch type
                                if '@pitch_type' in pi.keys():
                                    pt = pi['@pitch_type']
                                    for poss in pitch_possibilities:
                                        pitch_dic = dic[pitcher][poss[0]]
                                        for t in poss:
                                            if pt == t:
                                                dic[pitcher]['total'] += 1.0
                                                pitch_dic['counter'] += 1.0
                                                for att in attributes_list:
                                                    # print pi[att]
                                                    pitch_dic[att] += float(pi[att])                                          

    return dic

def dict_to_list(dic):   
    results = []
    for player, attributes in dic.items():
        vector = {}
        total = attributes['total']
        vector['total'] = total
        attributes_list = ['@break_angle', '@break_length', '@break_y', '@pfx_x', '@pfx_z', '@spin_dir', '@spin_rate', '@start_speed', '@x0', '@y0', '@z0']
        pitch_type_list = ['FF','FT','FC','SI','SF','SL','CH','CB','KC','KN','EP']
        attributes['handedness'] = {}
        handedness = attributes['handedness']
        if handedness == 'L':
            vector['handedness']['L'] = 1
            vector['handedness']['R'] = 0
        elif handedness == 'R':
            vector['handedness']['L'] = 0
            vector['handedness']['R'] = 1
        for pt in pitch_type_list:
            vector[pt] = {}
            vector[pt]['counter'] = attributes[pt]['counter']
            for att in attributes_list:
                if attributes[pt]['counter'] == 0:
                    vector[pt][att] = 0.0
                else:
                    vector[pt][att] = attributes[pt][att] / attributes[pt]['counter']
        tup = (player, vector)
        results.append(tup)
    return results

def main_function():
    dictionary = {}
    curr = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(curr, "june_data")
    for root, dirs, filenames in os.walk(folder):
        for game_file in filenames:
            name = os.path.join(folder, game_file)
            if name.endswith('.json'):
                dictionary = produce_results(dictionary, name)
    results = dict_to_list(dictionary)
    print results
    pickle.dump(results, open("results.p", "wb"))

main_function()
