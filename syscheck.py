import os
cmd="python sokoban.py --level=1 --last_level=2"
print(os.system(cmd))

solfile=open('sol.txt','r')
print(solfile.read())
