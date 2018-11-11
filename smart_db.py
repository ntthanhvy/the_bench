#!/usr/bin/env python3
import json
import sys


def load_query():
    # turn the query file into dict
    with open(sys.argv[-1], 'r') as f:
        return json.load(f)


# ------------compare two condition of the query------
def compare(a, b, op):
    # if the data is an digit turn it into interger
    if a.isdigit() and b.isdigit():
        a = int(a)
        b = int(b)
    if op == '=':
        return a == b
    elif op == '<':
        return a < b
    elif op == '>':
        return a > b
    elif op == '!=':
        return a != b


# -----------get the compare value and compare------------
def do_query(query, data, pos):
    for x in pos:
        if x in query['left']:
            # if there are a first_letter in the query compare the first value
            if 'first_letter' in query['left']:
                value = data[pos[x]][0]
            else:  # if not compare the whole data
                value = data[pos[x]]
            return compare(value, query['right'], query['op'])


# --------------get the result-----------------------
def search(pos, query):
    result = []
    # line = sys.stdin.readline()  # read the stdin
    # count = 0
    # # while the stdin is not empty do the query stop when it empty
    # while line:
    #     data = line.split(',')
    #     data[5] = data[5][:-1]  # remove the '\n' at the end of the line
    #     if 'where_and' in query.keys():  # do query with the where_and
    #         for q in query['where_and']:
    #             if not do_query(q, data, pos):
    #                 break
    #     elif 'where_or' in query.keys():  # do the query with where_or
    #         for q in query['where_or']:
    #             if not do_query(q, data, pos):
    #                 break
    #     result.append(data)
    #     line = sys.stdin.readline()
    #     count += 1
    # print(len(result))
    '''order option of result from query'''
    lines = sys.stdin.readlines()
    for line in lines:
        data = line.split(',')
        data[5] = data[5][:-1]  # remove the '\n' at the end of the line
        if 'where_and' in query.keys():  # do query with the where_and
            for q in query['where_and']:
                if not do_query(q, data, pos):
                    break
        elif 'where_or' in query.keys():  # do the query with where_or
            for q in query['where_or']:
                if not do_query(q, data, pos):
                    break
        result.append(data)
    return result


# ----------print the result to the screen------------------
def output(result, query, pos):
    s = query['select'].split(', ')
    p = [pos[x] for x in s]
    for l in result:  # return the select field
        r = []
        for a in l:
            if l.index(a) in p:
                r.append(a)
        print(', '.join(r))


# ---------the main function-------------------------------
def main():
    # set up the keywords position in the data
    pos = {'first_name': 0, 'last_name': 1, 'username': 2, 'age': 3,
           'gender': 4, 'city': 5}
    querys = load_query()
    for query in querys:
        result = search(pos, query)
        # check for the order
        if 'order' in query.keys():
            if query['order'] == 'age':
                # if order by age turn the str to interger
                result.sort(key=lambda x: int(x[pos['age']]))
            result.sort(key=lambda x: x[pos[query['order']]])
        output(result, query, pos)


main()
