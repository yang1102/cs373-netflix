#!/usr/bin/env python3

# ------------------------------
# projects/netflix/RunNetflix.py
# Copyright (C) 2016
# Shuoyi Yang, Chuqi Zhou
# ------------------------------

# -------
# imports
# -------

import sys


from Netflix import netflix_solve

# ----
# main
# ----

if __name__ == "__main__":
    netflix_solve(sys.stdin, sys.stdout)
# netflix_rmse()
