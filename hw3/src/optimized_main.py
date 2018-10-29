"""Recommender Systems."""

from scipy import spatial
from collections import OrderedDict, Counter, defaultdict

import sys
import math
import numpy as np


def read_input():
    """
    Read input from stdin.

    The first line of the input contains 2 space seperated integers R M.
        R is the number of lines of rating information.
        M is the number of movies.
    Next R lines contain the rating information.
        Each line will contain 3 space seperated values (user id, movie id, rating).
    Next M lines contain the metadata information.
        The first word/value of each line is the movie id.
        The rest of the words are the metadata information about that movie.
    The last line with contain 2 space seperated integers (target user id, target movie id)
        for which you need to estimate the rating.
    """
    with open("../data/sampleInput.txt") as f:
        first_line = f.readline().rstrip("\n").split(" ")

        # number of rating information
        global R, M
        R = int(first_line[0])

        # total number of movies
        M = int(first_line[1])

        user_ids = []
        movie_ids = []
        ratings = []

        # R(m) is the set of users that have rated the movie m in the available dataset. Rm[movie] = list of users
        Rm = defaultdict(list)

        # R(u) are the set of the movies that have been rated by the user u.  Ru[user] = list of movies
        Ru = defaultdict(list)

        # user -> movie relation
        rating_dict = {}
        user_movie = defaultdict(list)
        user_ratings = defaultdict(list)
        movie_ratings = defaultdict(list)

        for _ in range(R):
            rating_info = f.readline().rstrip("\n").split(" ")
            user_id, movie_id, rating = int(rating_info[0]), int(rating_info[1]), float(rating_info[2])
            rating_dict[(user_id, movie_id)] = rating
            user_movie[user_id].append(movie_id)
            movie_ratings[movie_id].append(rating)
            user_ratings[user_id].append(rating)

            # mapping from movie to the users rated this movie
            Rm[movie_id].append(user_id)

            # mapping from user to the movies this user rated
            Ru[user_id].append(movie_id)

            user_ids.append(user_id)
            movie_ids.append(movie_id)
            ratings.append(rating)

        # µ is the global mean calculated across all the ratings available
        global mu
        mu = sum(ratings) / len(ratings)

        movie_meta_info = {}
        word_movie = defaultdict(set)
        for _ in range(M):
            meta_info = f.readline().rstrip("\n").split(' ')
            term_index_dict = defaultdict(int)
            for word in meta_info[1:]:
                word_movie[word].add(int(meta_info[0]))
                term_index_dict[word] += 1
            movie_meta_info[int(meta_info[0])] = dict(term_index_dict)

        words = list(word_movie.keys())
        global V
        V = len(word_movie)
        term_index = {}
        for idx, word in enumerate(words):
            term_index[word] = idx

        last_line = f.readline().rstrip("\n").split(" ")
        global target_user_id, target_movie_id
        target_user_id, target_movie_id = int(last_line[0]), int(last_line[1])

    return rating_dict, Rm, Ru, movie_ratings, user_ratings, movie_meta_info, word_movie, term_index, user_movie, movie_ratings


def main():
    """Main pipeline for Recommender Systems."""
    rating_dict, Rm, Ru, movie_ratings, user_ratings, movie_meta_info, word_movie, term_index, user_movie, movie_ratings = read_input()

    # get target user rated movies
    rated_movies = Ru[target_user_id]

    # bm_dict = {}
    # target_movie_rating = movie_ratings[target_movie_id]
    # bm_dict[target_movie_id] = np.sum(np.array(target_movie_rating) - mu) / len(target_movie_rating)
    # b_m = bm_dict[target_movie_id]

    # for m_ in rated_movies:
    #     up = 0.
    #     if m_ in bm_dict:
    #         bm = bm_dict[m_]
    #     else:
    #         m_rating = movie_ratings[m_]
    #         bm_dict[m_] = np.sum(np.array(m_rating) - mu) / len(m_rating)
    #         bm = bm_dict[m_]
    #     up += rating_dict[(target_user_id, m_)] - mu - bm
    # b_u = up / len(rated_movies)
    bm_dict = defaultdict(float)
    b_um = cal_b_m(movie_ratings, rating_dict, user_ratings, bm_dict, user_movie, target_movie_id, target_user_id)
    # b_um = mu + b_u + b_m
    # print(b_um)

    s_mj = []
    d_target = cal_dv(movie_meta_info, word_movie, term_index, target_movie_id)

    for j in rated_movies:
        d_j = cal_dv(movie_meta_info, word_movie, term_index, j)
        s_mj.append(1 - spatial.distance.cosine(d_target, d_j))

    up = []
    for j in range(len(rated_movies)):
        r_uj = rating_dict[(target_user_id, rated_movies[j])]
        b_uj = cal_b_m(movie_ratings, rating_dict, user_ratings, bm_dict, user_movie, rated_movies[j], target_user_id)
        up.append(s_mj[j] * (r_uj - b_uj))

    result = np.sum(up) / np.sum(s_mj)

    # print(result)
    print(round(b_um + result, 1))


def cal_b(movie_ratings, bm_dict, m_id):
    """"""
    m_rating = movie_ratings[m_id]
    res = np.sum(np.array(m_rating) - mu) / len(m_rating)
    bm_dict[m_id] = res
    return res


def cal_b_m(movie_ratings, rating_dict, user_ratings, bm_dict, user_movie, target_movie_id, target_user_id):
    """"""
    if target_movie_id in bm_dict:
        b_m = bm_dict[target_movie_id]
    else:
        b_m = cal_b(movie_ratings, bm_dict, target_movie_id)
    # b_m = bm(target_movie_id) #-1.4
    movie_list = user_movie[target_user_id]
    up = []
    up = 0
    for m_id in movie_list:
        if m_id in bm_dict:
            val = bm_dict[m_id]
        else:
            val = cal_b(movie_ratings, bm_dict, m_id)
        up += rating_dict[(target_user_id, m_id)] - mu - val
    b_u = up / len(user_ratings[target_user_id])
    return mu + b_u + b_m


def cal_dv(movie_meta_info, word_movie, term_index, m_id):
    """"""
    tf_vector = np.zeros(V)
    idf_vector = np.zeros(V)
    t = movie_meta_info[m_id].keys()
    total = sum(movie_meta_info[m_id].values())
    for i in t:
        tf_vector[term_index[i]] = movie_meta_info[m_id][i] / total
        idf_vector[term_index[i]] = math.log(M / len(word_movie[i]))
    tmp = np.array(tf_vector) * np.array(idf_vector)
    return tmp.tolist()


if __name__ == '__main__':
    main()
