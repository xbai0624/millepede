
import sys, os
module_path = os.path.abspath("../core")
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from text_parser import vec3_t

import re
def parse_line(line):
    pattern = r'[,\s:()]+'
    fields = re.split(pattern, line)
    fields = [part for part in fields if part]
    #print(fields)

    if len(fields) != 22:
        print("ERROR: FAILED parsing line: ", line)

    res = []
    res.append(vec3_t(float(fields[9]), float(fields[10]), float(fields[11])))
    res.append(vec3_t(float(fields[14]), float(fields[15]), float(fields[16])))
    res.append(vec3_t(float(fields[19]), float(fields[20]), float(fields[21])))
    res.append(vec3_t(float(fields[4]), float(fields[5]), float(fields[6])))
    return res

def load_fermi_data(path="all_localHits_bestTrack.txt"):
    res = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i in lines:
            track = parse_line(i)
            res.append(track)
    return res


'''
# unit test
tracks = load_data()
for i in tracks:
    for j in i:
        print(j)
'''
