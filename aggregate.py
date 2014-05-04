import os, json
import numpy as np
import pickle


curr = os.path.dirname(os.path.realpath(__file__))
f=open(os.path.join(curr, "test.json"),"r+")
# i = 0
# for line in f:
#     print line
#     i = i + 1
#     if i > 1:
#         break
# f.close()
def get_data():
    data = json.load(f)
    f.close()
    return data

def produce_results():
    #structure of each pitcher: tuple (pitcher_id, [vector of attributes])
    results = [] #this will be the list of pitchers
    dic = {} #this will be our working dictionary of pitchers that will be transcribed to the results list
    data = get_data()['game']
    inning = data['inning']
    for inn in inning:
        top = inn['top']
        bottom = inn['bottom']
        for x in [top, bottom]:
            l = x['atbat']
            for m in l:
                pitcher = m['@pitcher']
                pitch = m['pitch']
                if pitcher not in dic:
                    dic[pitcher] = {}
                    dic[pitcher]['pitch_type'] = {}
                    pitch_type = dic[pitcher]['pitch_type']
                    pitch_type['FF'] = 0
                    pitch_type['FT'] = 0
                    pitch_type['FC'] = 0
                    pitch_type['SI'] = 0
                    pitch_type['SF'] = 0
                    pitch_type['SL'] = 0
                    pitch_type['CH'] = 0
                    pitch_type['CB'] = 0
                    pitch_type['KC'] = 0
                    pitch_type['KN'] = 0
                    pitch_type['EP'] = 0
                    pitch_type['total'] = 0.0
                if isinstance(pitch, dict):
                    pt = pitch['@pitch_type']
                    if pt == 'FF' or pt == 'FA':
                        pitch_type['FF'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'FT':
                        pitch_type['FT'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'FC':
                        pitch_type['FC'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'SI' or pt == 'FS':
                        pitch_type['SI'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'SF':
                        pitch_type['SF'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'SL':
                        pitch_type['SL'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'CH':
                        pitch_type['CH'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'CB' or pt == 'CU':
                        pitch_type['CB'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'KC':
                        pitch_type['KC'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'KN':
                        pitch_type['KN'] += 1
                        pitch_type['total'] += 1
                    elif pt == 'FT':
                        pitch_type['EP'] += 1
                        pitch_type['total'] += 1
                    # else:
                    #     print pt
                else:    
                    for pi in pitch:
                        pt = pi['@pitch_type']
                        if pt == 'FF' or pt == 'FA':
                            pitch_type['FF'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'FT':
                            pitch_type['FT'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'FC':
                            pitch_type['FC'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'SI' or pt == 'FS':
                            pitch_type['SI'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'SF':
                            pitch_type['SF'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'SL':
                            pitch_type['SL'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'CH':
                            pitch_type['CH'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'CB' or pt == 'CU':
                            pitch_type['CB'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'KC':
                            pitch_type['KC'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'KN':
                            pitch_type['KN'] += 1
                            pitch_type['total'] += 1
                        elif pt == 'FT':
                            pitch_type['EP'] += 1
                            pitch_type['total'] += 1
                        # else:
                        #     print pt
                        # else:
                        #     print pt
                    # else:
                    #     print pi + " is not dictionary!"
    for player, attributes in dic.items():
        pitch_type_dic = attributes['pitch_type']
        pitch_total = pitch_type_dic['total']
        vector = []
        vector.append(pitch_type_dic['FF']/ pitch_total)
        vector.append(pitch_type_dic['FT']/ pitch_total)
        vector.append(pitch_type_dic['FC']/ pitch_total)
        vector.append(pitch_type_dic['SI']/ pitch_total)
        vector.append(pitch_type_dic['SF']/ pitch_total)
        vector.append(pitch_type_dic['SL']/ pitch_total)
        vector.append(pitch_type_dic['CH']/ pitch_total)
        vector.append(pitch_type_dic['CB']/ pitch_total)
        vector.append(pitch_type_dic['KC']/ pitch_total)
        vector.append(pitch_type_dic['KN']/ pitch_total)
        vector.append(pitch_type_dic['EP']/ pitch_total)
        # print (player, vector)
        vector = np.array(vector, float)
        tup = (player, vector)
        results.append(tup)
    return results 





    
results = produce_results()
pickle.dump(results, open("results.p", "wb"))
# print results[0]


# print data['game']
# for key in data['game']:
#     print key
# for line in f:
#     print line
#     data = json.load(line)
#     print data