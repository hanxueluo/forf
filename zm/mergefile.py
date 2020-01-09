#!/usr/bin/python
import glob
import re
import sys

def f1():
    res = {}
    for fn, _ in file_list:
        c = ""
        with open(fn, "r") as f:
            c = f.read()

        res.setdefault("==HEADER", []).append(fn)
        for l in c.splitlines():
            l = l.strip()
            if not l: continue
            ls =  l.split("\t", 2)
            if len(ls) != 2:
                print "Invalid line: %s in file %s" % (l, fn)
            res.setdefault(ls[0], []).append(ls[1])


def find_files(prefix):
    file_list = []

    for fn in glob.glob(prefix+"*"):
        index = 0
        reg = re.match('\w+ (\d+)', fn)
        if reg:
            index = int(reg.group(1))
        file_list.append((fn, index))

    file_list.sort(key=lambda x: x[1])
    return file_list

def output(files, outfile):
    res = {}
    for fn, _ in files:
        c = ""
        with open(fn, "r") as f:
            c = f.read()

        for l in c.splitlines():
            l = l.strip()
            if not l: continue
            ls =  l.split("\t", 2)
            if len(ls) != 2:
                print "Invalid line: %s in file %s" % (l, fn)
            r = res.setdefault(ls[0], {})
            r[fn] = ls[1]
    keys = [ k for k in res.iterkeys() ]
    keys.sort()

    s = "-\t"
    for fn, _ in files:
        s += fn.split(".")[0] + "\t"
    s = s.rstrip() + "\n"

    for k in keys:
        s += k + "\t"
        for fn, _ in files:
            s += res.get(k, {}).get(fn, "0") + "\t"
        s = s.rstrip() + "\n"

    with open(outfile, "w") as f:
        f.write(s)

files = find_files(sys.argv[1])
print "Files: ", ", ".join([ a[0] for a in files ])

output(files, "_out.txt")
