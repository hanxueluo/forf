#!/usr/bin/python

import os
import sys
import time
import shutil

def load_key_value_file(filename):
    res = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            items = line.split("\t", 1)
            if len(items) != 2:
                raise Exception('Bad format in line "%s"' % line)
            res[items[0]] =items[1]
    return res

def load_filter_file(filename):
    res = set()
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().strip('"')
            if not line:
                continue
            items = line.split("\t", 1)[0]
            res.add(items)
    return res


def run(f1, f2, f3=""):
    outfilename = time.strftime("output_%Y%m%d%H%M%S.csv")
    dict2 = load_key_value_file(f2)
    dict1 = load_key_value_file(f1)
    filter_key = set()
    if f3 and os.path.isfile(f3):
        filter_key = load_filter_file(f3)

    if filter_key:
        dict1 = dict(filter(lambda kv: kv[1] in filter_key, dict1.iteritems()))

    res = {}
    allv2 = set()
    for k, v1 in dict1.iteritems():
        v2 = dict2.get(k, None)
        if not v2:
            continue
        allv2.add(v2)
        v1dict = res.setdefault(v1, {})
        count = v1dict.setdefault(v2, 0)
        v1dict[v2] = count + 1

    for k in filter_key:
        res.setdefault(k, {})

    print "line * column: %s * %s" % (len(res), len(allv2))
    write_file(outfilename, res, allv2)
    return res

def write_file(outfilename, res, allv2):
    l = list(allv2)
    s = "," + ",".join(l) + "\n"
    for k, v in res.iteritems():
        s += k + ","
        for c in l:
            s += str(v.get(c, 0)) + ","
        s += "\n"
    with open("tmp.output", "w") as f:
        f.write(s)
    shutil.move("tmp.output", outfilename)

def main():
    if len(sys.argv) < 3:
        print "Usage: %s file1 file2 [file3]" % sys.argv[0]
        sys.exit(1)
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    file3 = sys.argv[3] if len(sys.argv) >= 4 else None
    run(file1, file2, file3)

main()
