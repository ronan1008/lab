filepath = '/Users/shocklee/Desktop/ipfile'
with open(filepath, 'r') as f:
    for i, line in enumerate(f.readlines()):
        i+=1
        ip = line.strip().split(',')
        if i % 10 == 1 and i!= 1:
            print('')
        ipAddr = ip[1]
        print("host{:03d} = {}".format( i, ipAddr))
