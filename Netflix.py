#!/usr/bin/env python3

# ------------------------------
# projects/netflix/Netflix.py
# Copyright (C) 2016
# Shuoyi Yang, Chuqi Zhou
# ------------------------------

import pickle
# import os
# import sys
from urllib.request import urlopen
from math import sqrt
from numpy import mean, sqrt, square, subtract


# BASE_PATH = '/u/downing/cs/netflix-caches/'
BASE_URL = 'http://www.cs.utexas.edu/users/downing/netflix-caches/'
CACHE_NAME = {
    'answer': 'amm6364-answer.p', 'cRatingCache': 'amm6364-averageCustomerRating.p',
    'mRatingCache': 'amm6364-averageMovieRating.p', 'mYear': 'bdd465-movieYear.p'}


# no order
def netflix_read(line):
    cId = []
    line = line.split()
    fId = int(line[0].strip(':'))
    cId += [int(i) for i in line[1:]]
    # try:
    #     fId = int(line[0].strip(':'))
    #     raise ValueError('invalid film id')
    # except ValueError:
    #     print('invalid film id')
    #     return
    # try:
    #     cId += [int(i) for i in line[1:]]
    #     raise ValueError('invalid film id')
    # except ValueError:
    #     print('invalid customer name')
    #     return
    return fId, cId


def netflix_print(writer, fId, predRate):
    output = ''
    for i in predRate:
        output += str(format(i, '.1f')) + '\n'
    # writer.write(str(fId)+':\n'+ output+'\n\nRMSE:'+str(rmse)+'\n\n')
    writer.write(str(fId) + ':\n' + output)


def netflix_eval(fId, cId, cache):
    # preditciont alg 1
    '''
    get avg rating for the movie and avg rating for customer
    avg it
    '''
    cRatingCache = cache['cRatingCache']
    mRatingCache = cache['mRatingCache']
    result = []
    for i in cId:
        predRate = round((cRatingCache[i] + mRatingCache[fId]) / 2, 1)
        assert(1 <= predRate <= 5)
        result += [predRate]
    return result
    # return [(cRatingCache[i]+mRatingCache[fId])/2 for i in cId]


def netflix_load_cache(name):
    # filepath = BASE_PATH + CACHE_NAME[name]
    # if os.path.isfile(filepath):
    #     f = open(filepath, 'rb')
    #     cache = pickle.load(f)
    #     f.close()
    # else:
    cache_read_from_url = urlopen(BASE_URL + CACHE_NAME[name]).read()
    cache = pickle.loads(cache_read_from_url)
    return cache


# print for each film
# def each_netflix_rmse(cache, predict, fId, cId):
#     answer = cache['answer'][fId]
#     actual = [answer[i] for i in cId]
#     return sqrt(mean(square(subtract(actual, predict))))


def netflix_rmse(cache, predict, fId, cId):
    answer = cache['answer'][fId]
    actual = [answer[i] for i in cId]
    return list(square(subtract(actual, predict)))


def netflix_solve(reader, writer):
    readlist = []
    rmse = []
    num = 0
    cache = {name: netflix_load_cache(name) for name in CACHE_NAME}
    for i in reader:
        if ':' in i:
            line = i
            readlist += [line]
            num += 1
        else:
            readlist[num - 1] += i
    for line in readlist:
        fId, cId = netflix_read(line)
        predRate = netflix_eval(fId, cId, cache)
        # rmse = each_netflix_rmse(cache,predRate,fId,cId)
        netflix_print(writer, fId, predRate)
        rmse += netflix_rmse(cache, predRate, fId, cId)
    writer.write('\nRMSE:' + str(format(round(sqrt(mean(rmse)), 2), '.2f')))
