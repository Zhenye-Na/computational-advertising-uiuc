"""Recommender Systems."""

import sys
import math
import collections
import numpy as np



# def read_input():
#     """
#     Read input from stdin.

#     Sample Inputs:
#         5 5
#         1 1 3.0
#         1 2 4.0
#         1 3 3.0
#         2 4 2.0
#         2 5 5.0
#         1 batman robin superhero
#         2 batman dark knight
#         3 dark knight returns
#         4 batman joker gotham
#         5 batman superhero
#         1 4

#     The first line of the input contains 2 space seperated integers R M.
#         R is the number of lines of rating information.
#         M is the number of movies.
#     Next R lines contain the rating information.
#         Each line will contain 3 space seperated values (user id, movie id, rating).
#     Next M lines contain the metadata information.
#         The first word/value of each line is the movie id.
#         The rest of the words are the metadata information about that movie.
#     The last line with contain 2 space seperated integers (target user id, target movie id)
#         for which you need to estimate the rating.
#     """
#     first_line = sys.stdin.readline().rstrip("\n").split(" ")
#     # number of rating information
#     R = int(first_line[0])

#     # total number of movies
#     global M
#     M = int(first_line[1])

#     user_ids = []
#     movie_ids = []
#     ratings = []

#     # R(m) is the set of users that have rated the movie m in the available dataset.
#     Rm = {}

#     # R(u) are the set of the movies that have been rated by the user u.
#     Ru = {}

#     # user -> movie relation
#     rating_dict = {}

#     for _ in range(R):
#         rating_info = sys.stdin.readline().rstrip("\n").split(" ")
#         user_id = int(rating_info[0])
#         movie_id = int(rating_info[1])
#         rating = float(rating_info[2])

#         rating_dict["{},{}".format(user_id, movie_id)] = rating

#         # mapping from movie to the users rated this movie
#         if movie_id not in Rm:
#             Rm[movie_id] = [user_id]
#         else:
#             Rm[movie_id].append(user_id)

#         # mapping from user to the movies this user rated
#         if user_id not in Ru:
#             Ru[user_id] = [movie_id]
#         else:
#             Ru[user_id].append(movie_id)

#         user_ids.append(user_id)
#         movie_ids.append(movie_id)
#         ratings.append(rating)

#     # µ is the global mean calculated across all the ratings available
#     mu = sum(ratings) / len(ratings)
#     user_ids = list(set(user_ids))
#     movie_ids = list(set(movie_ids))

#     movies = []
#     for _ in range(M):
#         meta_info = sys.stdin.readline().rstrip("\n").split(" ")
#         movie_id = int(meta_info[0])
#         movie_name = " ".join(meta_info[1:])
#         movies.append(movie_name)

#     last_line = sys.stdin.readline().rstrip("\n").split(" ")
#     target_user_id = int(last_line[0])
#     target_movie_id = int(last_line[1])

#     return target_user_id, target_movie_id, user_ids, movie_ids, rating_dict, Rm, Ru, mu, movies


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
    with open("../data/sampleInput.txt") as f:

        first_line = f.readline().rstrip("\n").split(" ")
        # number of rating information
        R = int(first_line[0])

        # total number of movies
        global M
        M = int(first_line[1])

        user_ids = []
        movie_ids = []
        ratings = []

        # R(m) is the set of users that have rated the movie m in the available dataset.
        Rm = {}

        # R(u) are the set of the movies that have been rated by the user u.
        Ru = {}

        # user -> movie relation
        rating_dict = {}

        for _ in range(R):
            rating_info = f.readline().rstrip("\n").split(" ")
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

            movie_ids.append(movie_id)
            user_ids.append(user_id)
            ratings.append(rating)

        # µ is the global mean calculated across all the ratings available
        mu = sum(ratings) / len(ratings)
        user_ids = set(user_ids)
        movie_ids = list(set(movie_ids))
        movie_ids.sort()

        global U
        U = len(user_ids)

        movies = []
        for _ in range(M):
            meta_info = f.readline().rstrip("\n").split(" ")
            movie_id = int(meta_info[0])
            movie_name = " ".join(meta_info[1:])
            movies.append(movie_name)

        last_line = f.readline().rstrip("\n").split(" ")
        target_user_id = int(last_line[0])
        target_movie_id = int(last_line[1])
        print("read finished")
        return target_user_id, target_movie_id, user_ids, movie_ids, rating_dict, Rm, Ru, mu, movies


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
    target_user_id, target_movie_id, user_ids, movie_ids, rating_dict, Rm, Ru, mu, movies = read_input()

    # rating matrix row -> users, column -> movies

    # For the (u, m) pairs not present in the data, we will use the formula below
    b_m = {}
    # for u_ in user_ids:
    for m_ in movie_ids:
        # Equation 3.
        # |Rm[m_]|: how many users have rated this movie
        length = len(Rm[m_])
        up = 0.
        for user in Rm[m_]:
            up += (rating_dict["{},{}".format(user, m_)] - mu)
            # column = rating_matrix[1:, m_][rating_matrix[1:, m_] != -1]
            # length = len(column)
            # s_r_um = np.sum(column)
        b_m[m_] = up / length

    print("b_m finished")

    b_u = {}
    for u_ in user_ids:
        for m_ in movie_ids:
            # Equation 4.
            # |R(u)|: how many movies this user rated
            if "{},{}".format(u_, m_) not in rating_dict:
                up = 0.
                length = len(Ru[u_])
                for movie in Ru[u_]:
                    up += rating_dict["{},{}".format(u_, movie)] - mu - b_m[movie]
                b_u[u_] = up / length

    print("b_u finished")

    b_um = {}
    for u_ in user_ids:
        for m_ in movie_ids:
            b_um["{},{}".format(u_, m_)] = mu + b_u[u_] + b_m[m_]

    print("b_um finished")

    # corpus -> movies list of movie names
    movie_names = ""
    for movie in movies:
        movie_names += (movie + " ")

    set_movie_names = list(set(movie_names.rstrip().split(" ")))
    matrix_movie_names = np.zeros((M + 1, len(set_movie_names)))
    for m_ in range(1, M + 1):
        for v_ in range(matrix_movie_names.shape[1]):
            matrix_movie_names[m_][v_] = tf(set_movie_names[v_], movies[m_ - 1].split(" ")) * idf(set_movie_names[v_ - 1], movies)

    print("matrix_movie_names finished")

    # Equation 1.
    result = b_um["{},{}".format(target_user_id, target_movie_id)]
    # s_mj = np.zeros((M + 1, M + 1))
    up = 0.
    s_mj = {}
    for j in Ru[target_user_id]:
        # s_mj[target_movie_id][j] = calculate_similarity(matrix_movie_names[target_movie_id], matrix_movie_names[j])
        s_mj[j] = calculate_similarity(matrix_movie_names[target_movie_id], matrix_movie_names[j])

    for j in Ru[target_user_id]:
        r_uj = rating_dict["{},{}".format(target_user_id, j)]
        b_uj = b_um["{},{}".format(target_user_id, j)]
        # r_uj = rating_matrix[target_user_id][j]
        # b_uj = b_um[target_user_id][j]
        up += s_mj[j] * (r_uj - b_uj)

    down = 0.
    for j in Ru[target_user_id]:
        down += s_mj[j]

    print(round(result + (up / down), 1))

if __name__ == '__main__':
    main()
