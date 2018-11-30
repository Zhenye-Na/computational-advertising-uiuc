"""Simple Recommender Systems."""

from scipy import spatial
from collections import defaultdict

import sys
import math
import numpy as np


def main():
    """Main pipeline for Simple Recommender Systems."""
    rating_dict, Rm, Ru, movie_ratings, user_ratings, movie_meta_info, word_movie_mapping, term_index, user_movie_mapping, movie_ratings = read_input()

    # get target user rated movies
    rated_target_movies = Ru[target_user_id]

    bm_mapping = defaultdict(float)
    b_um = cal_b_m(movie_ratings, rating_dict, user_ratings, bm_mapping, user_movie_mapping, target_movie_id, target_user_id)

    # calculate s_mj
    s_mj = []
    d_m = cal_dv(movie_meta_info, word_movie_mapping, term_index, target_movie_id)
    for j in rated_target_movies:
        d_j = cal_dv(movie_meta_info, word_movie_mapping, term_index, j)
        s_mj.append(1 - spatial.distance.cosine(d_m, d_j))

    up = []
    for j in range(len(rated_target_movies)):
        r_uj = rating_dict[(target_user_id, rated_target_movies[j])]
        b_uj = cal_b_m(movie_ratings, rating_dict, user_ratings, bm_mapping, user_movie_mapping, rated_target_movies[j], target_user_id)
        up.append(s_mj[j] * (r_uj - b_uj))

    result = np.sum(up) / np.sum(s_mj)
    result += b_um

    # print out
    print(round(result, 1))


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
    first_line = sys.stdin.readline().rstrip("\n").split(" ")

    # number of rating information and total number of movies
    global R, M
    R, M = int(first_line[0]), int(first_line[1])

    user_ids = []
    movie_ids = []
    ratings = []

    # R(m) is the set of users that have rated the movie m in the available dataset. Rm[movie] = list of users
    Rm = defaultdict(list)

    # R(u) are the set of the movies that have been rated by the user u.  Ru[user] = list of movies
    Ru = defaultdict(list)

    # (user, movie) -> rating
    rating_dict = {}
    user_movie_mapping = defaultdict(list)
    user_ratings = defaultdict(list)
    movie_ratings = defaultdict(list)

    for _ in range(R):
        rating_info = sys.stdin.readline().rstrip("\n").split(" ")
        user_id, movie_id, rating = int(rating_info[0]), int(rating_info[1]), float(rating_info[2])

        rating_dict[(user_id, movie_id)] = rating
        user_movie_mapping[user_id].append(movie_id)
        movie_ratings[movie_id].append(rating)
        user_ratings[user_id].append(rating)

        # mapping from movie to the users rated this movie
        Rm[movie_id].append(user_id)

        # mapping from user to the movies this user rated
        Ru[user_id].append(movie_id)

        # user_ids, movie_ids, ratings
        user_ids.append(user_id)
        movie_ids.append(movie_id)
        ratings.append(rating)

    # µ is the global mean calculated across all the ratings available
    global mu
    mu = sum(ratings) / len(ratings)

    # get all the movies' words
    movie_meta_info = {}
    word_movie_mapping = defaultdict(set)
    for _ in range(M):
        meta_info = sys.stdin.readline().rstrip("\n").split(" ")
        word_dict = defaultdict(int)
        for word in meta_info[1:]:
            word_movie_mapping[word].add(int(meta_info[0]))
            word_dict[word] += 1
        movie_meta_info[int(meta_info[0])] = dict(word_dict)

    term_index = {}
    words = list(word_movie_mapping.keys())
    global V
    V = len(word_movie_mapping)
    for idx, word in enumerate(words):
        term_index[word] = idx

    last_line = sys.stdin.readline().rstrip("\n").split(" ")
    global target_user_id, target_movie_id
    target_user_id, target_movie_id = int(last_line[0]), int(last_line[1])

    return rating_dict, Rm, Ru, movie_ratings, user_ratings, movie_meta_info, word_movie_mapping, term_index, user_movie_mapping, movie_ratings


def cal_dv(movie_meta_info, word_movie_mapping, term_index, m_id):
    """
    Convert metadata document for movie m into |V| dimensional vector d^m.

    together with tf-idf calculation
    """
    tf_vector, idf_vector = np.zeros(V), np.zeros(V)

    words = movie_meta_info[m_id].keys()
    total = sum(movie_meta_info[m_id].values())

    for word in words:
        # tf vector
        tf_vector[term_index[word]] = movie_meta_info[m_id][word] / total
        # idf vector
        idf_vector[term_index[word]] = math.log(M / len(word_movie_mapping[word]))

    d_m = tf_vector * idf_vector
    return d_m.tolist()


def cal_b(movie_ratings, bm_mapping, m_id):
    """Equation 4."""
    m_id_rates = movie_ratings[m_id]
    val = np.sum(np.array(m_id_rates) - mu) / len(m_id_rates)
    bm_mapping[m_id] = val
    return val


def cal_b_m(movie_ratings, rating_dict, user_ratings, bm_mapping, user_movie_mapping, m_id, u_id):
    """
    Calculate b_m.

    Equation 3.
    """
    if m_id in bm_mapping:
        b_m = bm_mapping[m_id]
    else:
        b_m = cal_b(movie_ratings, bm_mapping, m_id)

    movie_lists = user_movie_mapping[u_id]
    up = []
    up = 0
    for m_id in movie_lists:
        if m_id in bm_mapping:
            val = bm_mapping[m_id]
        else:
            val = cal_b(movie_ratings, bm_mapping, m_id)
        up += rating_dict[(u_id, m_id)] - mu - val
    b_u = up / len(user_ratings[u_id])
    return mu + b_u + b_m


if __name__ == '__main__':
    main()
