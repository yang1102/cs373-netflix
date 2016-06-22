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
    'answer': 'bis266-probeAns.p',
    'm_rating_cache': 'amm6364-averageMovieRating.p',
    'm_year': 'bdd465-movieYear.p',
    'avg_year': 'sy6955-avgUserFiveYears.p'}


# no order
def netflix_read(line):
    customer_id = []
    line = line.split()
    try:
        film_id = int(line[0].strip(':'))
    except ValueError:
        film_id = -1
    try:
        customer_id += [int(i) for i in line[1:]]
    except ValueError:
        customer_id = [-1]
    # assert the film_id and customer_id is valid
    assert film_id != -1 or customer_id != [-1]
    return film_id, customer_id


def netflix_print(writer, film_id, pred_rate):
    output = ''
    for i in pred_rate:
        output += format(i, '.1f') + '\n'
    writer.write(str(film_id) + ':\n' + output)


# find the rating of movieA (with given film_id) first, and
# find the average rating of all movies this customer has rated
# in a 5-year span where movieA is in.
def netflix_eval(film_id, customer_id, cache):
    '''
    get avg rating for the movie and avg rating for year
    avg it
    '''
    m_rating_cache = cache['m_rating_cache']
    m_year = cache['m_year']
    avg_year = cache['avg_year']
    result = []
    pred_rate = 0
    for i in customer_id:
        movie_year = m_year[film_id]
        if movie_year == 'NULL':
            pred_rate = round(
                (avg_year[i][movie_year] + m_rating_cache[film_id]) / 2, 1)

        else:
            movie_year = int(movie_year)
            for year in avg_year[i]:
                if year != 'NULL' and (movie_year in range(year, year + 5)):
                    pred_rate = round(
                        (avg_year[i][year] + m_rating_cache[film_id]) / 2, 1)

        assert 1 <= pred_rate <= 5
        result += [pred_rate]
    return result


def netflix_load_cache(name):
    cache_read_from_url = urlopen(BASE_URL + CACHE_NAME[name]).read()
    cache = pickle.loads(cache_read_from_url)
    return cache

# compute the RMSE.


def netflix_rmse(answer, predict):

    return round(sqrt(mean(square(subtract(answer, predict)))), 2)


def netflix_solve(reader, writer):
    readlist = []
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
        film_id, customer_id = netflix_read(line)
        pred_rate = netflix_eval(film_id, customer_id, cache)
        netflix_print(writer, film_id, pred_rate)
        answer += [cache['answer'][film_id][i] for i in customer_id]
        predict += pred_rate
    writer.write('\nRMSE:' +
                 format(netflix_rmse(answer, predict), '.2f') + '\n')
