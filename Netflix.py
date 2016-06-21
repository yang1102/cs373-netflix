#!/usr/bin/env python3

# ------------------------------
# projects/netflix/Netflix.py
# Copyright (C) 2016
# Shuoyi Yang, Chuqi Zhou
# ------------------------------

import pickle
from urllib.request import urlopen
from math import sqrt
from numpy import mean, sqrt, square, subtract


BASE_URL = 'http://www.cs.utexas.edu/users/downing/netflix-caches/'
CACHE_NAME = {
    'answer': 'bis266-probeAns.p', 'mRatingCache': 'amm6364-averageMovieRating.p',
    'mYear': 'bdd465-movieYear.p', 'avgYear': 'sy6955-avgUserFiveYears.p'}


# no order
def netflix_read(line):
    cId = []
    line = line.split()
    # fId = int(line[0].strip(':'))
    # cId += [int(i) for i in line[1:]]
    try:
        fId = int(line[0].strip(':'))
    except ValueError:
        fId = -1
    try:
        cId += [int(i) for i in line[1:]]
    except ValueError:
        cId = -1
    # assert the fId and cId is valid
    assert(fId != -1 or cId != -1)
    return fId, cId


def netflix_print(writer, fId, predRate):
    output = ''
    for i in predRate:
        output += format(i, '.1f') + '\n'
    writer.write(str(fId) + ':\n' + output)


# def netflix_eval(fId, cId, cache):
# preditciont alg 1
#     '''
#     get avg rating for the movie and avg rating for customer
#     avg it
#     '''
#     cRatingCache = cache['cRatingCache']
#     mRatingCache = cache['mRatingCache']
#     result = []
#     for i in cId:
#         predRate = round((cRatingCache[i] + mRatingCache[fId]) / 2, 1)
#         assert(1 <= predRate <= 5)
#         result += [predRate]
#     return result
#     return [(cRatingCache[i]+mRatingCache[fId])/2 for i in cId]

def netflix_eval(fId, cId, cache):
    # preditciont alg 1
    '''
    get avg rating for the movie and avg rating for year
    avg it
    '''
    mRatingCache = cache['mRatingCache']
    mYear = cache['mYear']
    avgYear = cache['avgYear']
    result = []
    predRate = 0
    for i in cId:
        movie_year = mYear[fId]
        if movie_year == 'NULL':
            predRate = round(
                (avgYear[i][movie_year] + mRatingCache[fId]) / 2, 1)
            # predRate = (avgYear[i][movie_year]+ mRatingCache[fId]) / 2

        else:
            movie_year = int(movie_year)
            for year in avgYear[i]:
                if (year != 'NULL' and (movie_year in range(year, year + 5))):
                    predRate = round(
                        (avgYear[i][year] + mRatingCache[fId]) / 2, 1)
                    # predRate = (avgYear[i][year]+ mRatingCache[fId]) / 2
        assert(1 <= predRate <= 5)
        result += [predRate]
    return result


def netflix_load_cache(name):
    cache_read_from_url = urlopen(BASE_URL + CACHE_NAME[name]).read()
    cache = pickle.loads(cache_read_from_url)
    return cache


def netflix_rmse(answer, predict):

    return round(sqrt(mean(square(subtract(answer, predict)))), 2)


def netflix_solve(reader, writer):
    readlist = []
    rmse = []
    num = 0
    cache = {name: netflix_load_cache(name) for name in CACHE_NAME}
    answer = []
    predict = []
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
        netflix_print(writer, fId, predRate)
        answer += [cache['answer'][fId][i] for i in cId]
        predict += predRate
    writer.write('\nRMSE:' +
                 format(netflix_rmse(answer, predict), '.2f') + '\n')
