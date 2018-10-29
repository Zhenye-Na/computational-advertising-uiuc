"""Recommender Systems."""

import sys
import math
import collections
import numpy as np

from scipy import sparse


def read_input():
    """
    Read input from stdin.

    Sample Inputs:
        5 5
        1 1 3.0
        1 2 4.0
        1 3 3.0
        2 4 2.0
        2 5 5.0
        1 batman robin superhero
        2 batman dark knight
        3 dark knight returns
        4 batman joker gotham
        5 batman superhero
        1 4

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
    # number of rating information
    R = int(first_line[0])

    # total number of movies
    global M
    M = int(first_line[1])

    user_ids = []
    ratings = []

    # R(m) is the set of users that have rated the movie m in the available dataset.
    Rm = {}

    # R(u) are the set of the movies that have been rated by the user u.
    Ru = {}

    # user -> movie relation
    rating_dict = {}

    for _ in range(R):
        rating_info = sys.stdin.readline().rstrip("\n").split(" ")
        user_id = int(rating_info[0])
        movie_id = int(rating_info[1])
        rating = float(rating_info[2])

        rating_dict["{},{}".format(user_id, movie_id)] = rating

        # mapping from movie to the users rated this movie
        if movie_id not in Rm:
            Rm[movie_id] = [user_id]
        else:
            Rm[movie_id].append(user_id)

        # mapping from user to the movies this user rated
        if user_id not in Ru:
            Ru[user_id] = [movie_id]
        else:
            Ru[user_id].append(movie_id)

        user_ids.append(user_id)
        ratings.append(rating)

    # µ is the global mean calculated across all the ratings available
    mu = sum(ratings) / len(ratings)
    user_ids = list(set(user_ids))

    movies = []
    for _ in range(M):
        meta_info = sys.stdin.readline().rstrip("\n").split(" ")
        movie_id = int(meta_info[0])
        movie_name = " ".join(meta_info[1:])
        movies.append(movie_name)

    last_line = sys.stdin.readline().rstrip("\n").split(" ")
    target_user_id = int(last_line[0])
    target_movie_id = int(last_line[1])

    return target_user_id, target_movie_id, user_ids, rating_dict, Rm, Ru, mu, movies


def tf(t, m):
    """
    Term Frequency.

    tf(t,m) = Number of times term t appears in metadata of a movie m / Total number of terms in the metadata about m

    set_movie_names[v_] string
    movies[m_] list of strings
    """
    counter_t = collections.Counter(m)
    return counter_t[t] / len(m)


def idf(t, ms):
    """
    Inverse Document Frequency.

    idf(t) = ln(Total number of movies in dataset / Number of movies with term t in it)

    """
    counter = 0
    # print(ms)
    # print(t)
    for name in ms:
        if t in name:
            counter += 1

    return math.log(M / counter)


def calculate_similarity(d_m, d_j):
    """
    Cosine Similarity Calculation.

    Args:
        d_m:
        d_j:

    Returns:
        s_mj: the similarity value between 2 movies m and j.
    """
    return d_m.dot(d_j.T)


def main():
    """Main pipeline for Recommender Systems."""
    target_user_id, target_movie_id, user_ids, rating_dict, Rm, Ru, mu, movies = read_input()
    U = len(user_ids)

    # rating matrix row -> users, column -> movies
    rating_matrix = np.ones((U + 1, M + 1)) * -1
    for key, val in rating_dict.items():
        key_array = key.split(",")
        u = int(key_array[0])
        m = int(key_array[1])
        rating_matrix[u][m] = val

    num_of_row = rating_matrix.shape[0]
    num_of_col = rating_matrix.shape[1]
    # s_rating_matrix = sparse.csr_matrix(rating_matrix)

    # For the (u, m) pairs not present in the data, we will use the formula below
    b_m = {}
    for u_ in range(1, num_of_row):
        for m_ in range(1, num_of_col):
            # Equation 3.
            # |R(m)|: how many users have rated this movie
            column = rating_matrix[1:, m_][rating_matrix[1:, m_] != -1]
            length = len(column)
            s_r_um = np.sum(column)
            b_m[m_] = (s_r_um - length * mu) / length

    b_u = {}
    for u_ in range(1, num_of_row):
        for m_ in range(1, num_of_col):
            # Equation 4.
            # |R(u)|: how many movies this user rated
            if rating_matrix[u_][m_] == -1:
                row = rating_matrix[u_, 1:][rating_matrix[u_, 1:] != -1]
                s_r_um = np.sum(row)
                length = len(row)
                b_m_sum = 0
                for movie in Ru[u_]:
                    # if movie in b_m:
                    b_m_sum += b_m[movie]

                b_u[u_] = (s_r_um - length * mu - b_m_sum) / length

    # Equation 2.
    b_um = np.zeros((U + 1, M + 1))
    for u_ in range(1, b_um.shape[0]):
        for m_ in range(1, b_um.shape[1]):
            b_um[u_][m_] = mu + b_u[u_] + b_m[m_]

    # corpus -> movies list of movie names
    movie_names = ""
    for movie in movies:
        movie_names += (movie + " ")

    set_movie_names = list(set(movie_names.rstrip().split(" ")))
    matrix_movie_names = np.zeros((M + 1, len(set_movie_names)))
    for m_ in range(1, M + 1):
        for v_ in range(matrix_movie_names.shape[1]):
            matrix_movie_names[m_][v_] = tf(set_movie_names[v_], movies[m_ - 1].split(" ")) * idf(set_movie_names[v_ - 1], movies)

    # Equation 1.
    result = b_um[target_user_id][target_movie_id]
    # s_mj = np.zeros((M + 1, M + 1))
    up = 0.
    s_mj = {}
    for j in Ru[target_user_id]:
        s_mj[j] = calculate_similarity(matrix_movie_names[target_movie_id], matrix_movie_names[j])

    for j in Ru[target_user_id]:
        r_uj = rating_matrix[target_user_id][j]
        b_uj = b_um[target_user_id][j]
        up += s_mj[j] * (r_uj - b_uj)

    down = 0.
    for j in Ru[target_user_id]:
        down += s_mj[j]

    print(round(result + (up / down), 1))

if __name__ == '__main__':
    main()
