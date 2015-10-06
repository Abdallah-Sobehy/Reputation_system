# This file is meant to be executed after running: python -m cProfile -o main.profile main.py
import cProfile
import pstats
# create a file if does not exist ot override and existing one
#f_tottime = open('profile_tottime_op_localupdate1.txt','w')
f_cumtime = open('profile_cumtime_op_localupdate1.txt','w')
# to have the output saved in the file instead of the termina
#p_tot = pstats.Stats('main.profile',stream=f_tottime)
p_cum = pstats.Stats('main.profile',stream=f_cumtime)
# strp_dirs() the path in the function column which saves a lost of space in the file
#p_tot.strip_dirs().sort_stats('tottime').print_stats(0.5)
p_cum.strip_dirs().sort_stats('cumtime').print_stats(0.5)