import os

for filename in os.listdir('./parameters'):
   print(filename)
   exec(open('EvolutionDarwin.py').read(),{'argv':'./parameters/'+filename})