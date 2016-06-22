#!/usr/bin/env python3

# ------------------------------
# projects/netflix/TestNetflix.py
# Copyright (C) 2016
# Shuoyi Yang, Chuqi Zhou
# ------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase
from Netflix import netflix_read, netflix_print, netflix_eval
from Netflix import netflix_solve, netflix_load_cache, netflix_rmse

# -----------
# TestNetflix
# -----------


class TestNetflix (TestCase):

    # ----
    # read
    # ----

    def test_read_1(self):
        line = '1:\n30878\n2647871\n1283744\n2488120'
        i, j = netflix_read(line)
        self.assertEqual(i,  1)
        self.assertEqual(j, [30878, 2647871, 1283744, 2488120])

    # Test whitespace
    def test_read_2(self):
        line = '1:\n   30878\n  2647871\n 1283744   \n 2488120'
        i, j = netflix_read(line)
        self.assertEqual(i,  1)
        self.assertEqual(j, [30878, 2647871, 1283744, 2488120])

    # Test invalid film ID
    def test_read_3(self):
        line = 'a:\n   30878b\n  2647871d\n 1283744s   \n 2488120d'
        with self.assertRaises(AssertionError):
            netflix_read(line)

    # -----
    # print
    # -----
    def test_print_1(self):
        writer = StringIO()
        netflix_print(writer, 1, [1.1, 2.2, 3.3])
        self.assertEqual(writer.getvalue(), "1:\n1.1\n2.2\n3.3\n")

    # Test printing format (one decimal point)
    def test_print_2(self):
        writer = StringIO()
        netflix_print(writer, 17770, [1, 2, 3])
        self.assertEqual(writer.getvalue(), "17770:\n1.0\n2.0\n3.0\n")

    # ----
    # eval
    # ----
    def test_eval_1(self):
        cache = {'m_year': {1: 1984, 2: 1993, 3: 2003},
                 'm_rating_cache': {1: 4.2134, 2: 4.1235, 3: 2.6688},
                 'avg_year': {1000: {1980: 3.5432, 1990: 3.456},
                              2000: {1980: 4.217, 2000: 3.8864},
                              3000: {1980: 3.459, 1995: 4.0012}}}
        val = netflix_eval(1, [1000, 2000, 3000], cache)
        self.assertEqual(val, [3.9, 4.2, 3.8])

    # Test the predict rate range
    def test_eval_2(self):
        cache = {'m_year': {1: 1984, 2: 1993, 3: 2003},
                 'm_rating_cache': {1: 5.5678, 2: 4.1235, 3: 2.6688},
                 'avg_year': {1000: {1980: 5.5432, 1990: 3.456},
                              2000: {1980: 4.217, 2000: 3.8864},
                              3000: {1980: 3.459, 1995: 4.0012}}}
        with self.assertRaises(AssertionError):
            netflix_eval(1, [1000, 2000], cache)

    # Test the file movie year null
    def test_eval_3(self):
        cache = {'m_year': {1: 1984, 2: 'NULL', 3: 2003},
                 'm_rating_cache': {1: 4.2134, 2: 4.1235, 3: 2.6688},
                 'avg_year': {1000: {1980: 4.679, 1990: 3.456, 'NULL': 4.9875},
                              2000: {1980: 4.217, 2000: 3.8864},
                              3000: {1980: 3.459, 1995: 4.0012, 'NULL': 3.1248}}}
        val = netflix_eval(2, [1000, 3000], cache)
        self.assertEqual(val, [4.6, 3.6])

    # Test the customer saw null movie
    def test_eval_4(self):
        cache = {'m_year': {1: 1984, 2: 1927, 3: 2003},
                 'm_rating_cache': {1: 4.2134, 2: 4.1235, 3: 2.6688},
                 'avg_year': {1000: {1980: 4.679, 1990: 3.456, 'NULL': 4.9875},
                              2000: {1980: 4.217, 2000: 3.8864},
                              3000: {1980: 3.459, 1995: 4.0012, 'NULL': 3.1248}}}
        val = netflix_eval(1, [1000, 2000, 3000], cache)
        self.assertEqual(val,  [4.4, 4.2, 3.8])

    # ----------
    # cache_open
    # ----------
    def test_cache_open_1(self):
        key = "answer"
        cache = netflix_load_cache(key)
        self.assertEqual(len(cache), 16938)

    def test_cache_open_2(self):
        key = 'm_year'
        cache = netflix_load_cache(key)
        self.assertEqual(len(cache), 17770)

    def test_cache_open_3(self):
        key = 'avg_year'
        cache = netflix_load_cache(key)
        self.assertEqual(len(cache), 480189)

    def test_cache_open_4(self):
        key = 'm_rating_cache'
        cache = netflix_load_cache(key)
        self.assertEqual(len(cache), 17770)

    # -----
    # solve
    # -----
    def test_solve(self):
        reader = StringIO(
            '1:\n30878\n2647871\n1283744\n2488120\n317050\n1904905\n1989766')
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(
            writer.getvalue(), '1:\n3.7\n3.3\n3.8\n4.2\n3.9\n3.7\n3.1\n\nRMSE:0.75\n')

    # Test movie year is null 4388,NULL,Ancient Civilizations: Rome and Pompeii
    def test_solve_2(self):
        reader = StringIO(
            '4388:\n2493000\n1670719\n1359762\n1753674\n1815164')
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(
            writer.getvalue(), '4388:\n2.5\n3.5\n3.0\n2.0\n4.0\n\nRMSE:0.71\n')

    def test_solve_3(self):
        reader = StringIO(
            '10004:\n1737087\n1270334\n1262711\n1903515\n2140798\n2479158\n2161335')
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(
            writer.getvalue(), '10004:\n4.5\n4.2\n3.9\n4.0\n4.1\n4.0\n4.1\n\nRMSE:0.87\n')

    # -----
    # rmse
    # -----
    def test_rmse_1(self):
        error = netflix_rmse([1, 2, 3], [1, 2, 3])
        self.assertEqual(error, 0)

    # test the decimal rate
    def test_rmse_2(self):
        error = netflix_rmse([5, 6, 7], [9.0, 10.0, 11.0])
        self.assertEqual(error, 4.00)

    def test_rmse_3(self):
        error = netflix_rmse([4, 2, 3], [1, 2, 3])
        self.assertEqual(error, 1.73)


# ----
# main
# ----
if __name__ == "__main__":
    main()


""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
...................
----------------------------------------------------------------------
Ran 19 tests in 13.212s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          67      0     22      0   100%
TestNetflix.py      84      0      0      0   100%
------------------------------------------------------------
TOTAL              151      0     22      0   100%
"""
