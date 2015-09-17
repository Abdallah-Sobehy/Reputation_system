# This file is meant to be executed after running: python m- cProfile -o main.profile main .py
import cProfile
import pstats
# create a file if does not exist ot override and existing one
f = open('profile.txt','w')
# to have the output saved in the file instead of the termina
p = pstats.Stats('main.profile',stream=f)
# strp_dirs() the path in the function column which saves a lost of space in the file
p.strip_dirs().sort_stats('time').print_stats(5)
