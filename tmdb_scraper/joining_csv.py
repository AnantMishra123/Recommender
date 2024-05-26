import sys

def append_to_file(src, dst):
    with open(src, "r") as s:
        s.readline()
        content = s.read()
        with open (dst, "a") as d:
            d.write(content)

n = len(sys.argv)

for i in range(0, n):
    #print(sys.argv[i])
    append_to_file(sys.argv[i], sys.argv[1])

