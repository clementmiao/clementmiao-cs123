import sys
import random
import csv


# INITIALIZATION OF CENTROIDS


#Read from the csv and create dictionary. Format: {id:[attributes..]}
def readFile(file):
    big_list = []
    csvfile = open(file, 'r')
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        big_list.append(row)
    return big_list

def readMatchupsFile(file):
    big_list = {}
    csvfile = open(file, 'r')
    reader = csv.reader(csvfile, delimiter=',')
    j = 0
    for row in reader:
        tuple_list = []
        small_list = row[1:]
        player = row[0].split("\t")[0]
        # print player
        i = 0
        # print small_list
        for m in small_list:
            if i % 2 == 0:
                tuple = (small_list[i], small_list[i+1])
                tuple_list.append(tuple)
            i = i + 1
        # properties = {}
        # properties['list'] = tuple_list
        # properties['cluster'] = j
        # big_list[player] = properties
        big_list[player] = tuple_list
    return big_list
        # j = j + 1

def writeFile(file, li):
    txtfile = open(file,'w')
    txtfile.writelines(li)
    txtfile.close()    

def process(correct, wrong):
    master_list = []
    matches = set()
    for i in range(len(correct)):
        match = []
        index = -1
        for j in range(len(wrong)):
            element_a = correct[i]
            element_b = wrong[j]
            # total = maximum(len(element_a), len(element_b))
            intersection = set(element_a) & set(element_b)
            # shared = len(intersection) / total
            if len(intersection) > len(match):
                if j not in matches:
                    match = element_b
                    index = j
                    matches.add(index)
            # print matches

        if index != -1:
            master_list.append(index)
        else:

            master_list.append(-1)
    return master_list

def reorder(new_order, right_matchup_dict, matchup_dict):
    master_list = []
    for item in right_matchup_dict:
        if item in matchup_dict:
            total = 0
            li = []
            for i in range(len(new_order)):
                li.append(-1)
            element = matchup_dict[item]
            i = 0
            for ele in element:
                # print new_order
                new_index = new_order[i]
                if new_index != -1:
                    total = total + int(ele[1])
                    li[new_index] = ele
                i = i + 1
            for i in range(len(li)):
                if li[i] == -1:
                    li[i] = ('0','0')
            # print li
            string = item + "\t" + str(total)
            for i in li:
                string = string + "," + i[0] + "," + i[1] 
            master_list.append(string + "\n")
    return master_list



def maximum(a, b):
    if a > b:
        return a
    elif b > a:
        return b
    else:
        return a    

def main(argv):
    correct = readFile( argv[0] )
    # print correct
    wrong = readFile( argv[1] )
    # print wrong
    new_order = process(correct, wrong)
    matchup_dict = readMatchupsFile(argv[2] )
    right_matchup_dict = readMatchupsFile(argv[3])
    li = reorder(new_order, right_matchup_dict, matchup_dict)

    writeFile(argv[4], li)
    





main(sys.argv[1:])









