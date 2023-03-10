import os

for filename in os.listdir('.'):
   exec(open('../EvolutionDarwin.py').read(),"parameters/"+filename)