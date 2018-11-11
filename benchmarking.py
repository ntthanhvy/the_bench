#!/usr/bin/env python3

import subprocess
import argparse
import resource
import cProfile
import pstats
import importlib


# ---------------get args----------------------
def get_args():
    parser = argparse.ArgumentParser(prog='benchmarking.py')
    parser.add_argument('-m', action='store_true')
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-n', action='store_true')
    parser.add_argument('program', nargs='+')
    return parser.parse_args()


# -----------run subprocess--------------
def get_usage(args):
    # print(args)
    subprocess.run(args, stdout=subprocess.PIPE)
    return resource.getrusage(resource.RUSAGE_CHILDREN)


# -------------get memory of subprocess-----------------
def get_memory(usage):
    return 'Memory usage: %s KB' % (usage.ru_maxrss // 1024)


# ------------get running time of subprocess-------------
def get_time(usage):
    return 'Run time is: %s s' % (usage.ru_utime + usage.ru_stime)


# ------------get time call of a func in subprocess--------
def get_func_call(args):
    global file
    # get name of the subprocess
    file = args.program[0].strip('./').strip('.py')
    filename = 'stats.stats'  # create a file contain subprocess status
    cProfile.run('importlib.import_module(file)', filename)
    ps = pstats.Stats(filename).strip_dirs().sort_stats('time')
    ps.print_stats(args.program[0].strip('./').strip('.py'))


# -----------the main function--------------
def main():
    args = get_args()
    if args.m:  # the -m option
        usage = get_usage(args.program)  # get general usage
        print(get_memory(usage))  # print out the memory usage
    if args.n:  # the -n option
        print(get_func_call(args))  # get the time func call
    if args.t or not args.m or not args.n:
    # orther option include -t and no option
        usage = get_usage(args.program)
        print(get_time(usage))  # print the running time


main()
