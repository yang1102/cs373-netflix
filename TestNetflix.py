#!/usr/bin/env python3

# ------------------------------
# projects/netflix/netflix.py
# Copyright (C) 2016
# Shuoyi Yang, Chuqi Zhou
# ------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_print, netflix_eval, netflix_solve, netflix_load_cache, netflix_rmse

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
    # def test_read_3(self):
    #     line = 'a:\n   30878b\n  2647871d\n 1283744s   \n 2488120d'
    #     with self.assertRaises(ValueError):
    #         netflix_read(line)

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
        cache = {'cRatingCache': {1000: 2.1234, 2000: 3.1245, 3000: 4.1235},
                 'mRatingCache': {1: 3.5678, 2: 4.1235, 3: 2.6688}}
        val = netflix_eval(1, [1000, 2000, 3000], cache)
        self.assertEqual(val, [2.8, 3.3, 3.8])

    # Test the predict rate range
    def test_eval_2(self):
        cache = {'cRatingCache': {1000: 5.1234, 2000: 3.1245, 3000: 4.1235},
                 'mRatingCache': {1: 5.5678, 2: 4.1235, 3: 2.6688}}
        with self.assertRaises(AssertionError):
            netflix_eval(1, [1000, 2000], cache)

    def test_eval_3(self):
        cache = {'cRatingCache': {1000: 2.1234, 2000: 3.1245, 3000: 4.1235},
                 'mRatingCache': {1: 3.5678, 2: 4.1235, 3: 2.6688}}
        val = netflix_eval(2, [1000, 2000, 3000], cache)
        self.assertEqual(val, [3.1, 3.6, 4.1])

    # -----
    # solve
    # -----
    def test_solve(self):
        reader = StringIO(
            '1:\n30878\n2647871\n1283744\n2488120\n317050\n1904905\n1989766')
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(
            writer.getvalue(), '1:\n3.7\n3.5\n3.6\n4.2\n3.7\n3.8\n3.5\n\nRMSE:0.69')

    def test_solve2(self):
        reader = StringIO(
            '1000:\n2326571\n977808\n1010534\n1861759\n79755\n98259\n1960212\n97460\n2623506')
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(
            writer.getvalue(), '1000:\n3.4\n3.3\n3.1\n4.1\n3.7\n3.5\n3.5\n3.8\n3.3\n\nRMSE:1.07')

    # def test_solve3(self):
    #     reader = StringIO("100 199\n200 299\n300 399\n400 499\n")
    #     writer = StringIO()
    #     netflix_solve(reader, writer)
    #     self.assertEqual(
    # writer.getvalue(), "100 199 125\n200 299 128\n300 399 144\n400 499
    # 142\n")


# ----
# main
# ----

if __name__ == "__main__":
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
netflix          18      0      6      0   100%
Testnetflix      33      1      2      1    94%   79
---------------------------------------------------------
TOTAL            51      1      8      1    97%
"""
