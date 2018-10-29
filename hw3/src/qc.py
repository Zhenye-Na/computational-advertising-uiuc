from collections import defaultdict, Counter
from scipy import spatial
import math
import numpy as np

r, m = map(int, input().split(' '))
user_movie = defaultdict(list)
user_rating = defaultdict(list)
movie_rating = defaultdict(list)
movie_user = defaultdict(list)
um_rating = defaultdict(int)
movie_meta = dict()
term_movie = defaultdict(set)
rating = []
bm_dict = defaultdict(float)

for _ in range(r):
    tmp = input().split(' ')
    rating.append(float(tmp[2]))
    um_rating[(int(tmp[0]), int(tmp[1]))] = float(tmp[2])
    user_movie[int(tmp[0])].append(int(tmp[1]))
    movie_user[int(tmp[1])].append(int(tmp[0]))
    user_rating[int(tmp[0])].append(float(tmp[2]))
    movie_rating[int(tmp[1])].append(float(tmp[2]))

for _ in range(m):
    tmp = input().split(' ')
    term_dict = defaultdict(int)
    for term in tmp[1:]:
        term_movie[term].add(int(tmp[0]))
        term_dict[term] += 1
    movie_meta[int(tmp[0])] = dict(term_dict)


terms = list(term_movie.keys())
term_num = len(terms)
term_index = dict()
for ind, term in enumerate(terms):
    term_index[term] = ind
# term_index={'batman': 0, 'superhero': 1, 'robin': 3, 'gotham': 2, 'dark': 4, 'knight': 7, 'returns': 5, 'joker': 6}

movies = list(movie_meta.keys())
movie_num = len(movies)
target_user_id, target_movie_id = map(int, input().split(' '))
avg_rating = sum(rating)/len(rating)*1.0


print("avg: ", avg_rating)
# the set of the movies that have been rated by the user u.  [1, 2, 3]
R_u = user_movie[target_user_id]

# print user_movie,movie_user,user_rating,movie_rating
# um_rating :{(1, 2): 4.0, (2, 5): 5.0, (1, 3): 3.0, (1, 1): 3.0, (2, 4): 2.0}
# user_movie:{1: [1, 2, 3], 2: [4, 5]}
# movie_user:{1: [1], 2: [1], 3: [1], 4: [2], 5: [2]}
# user_rating:{1: [3.0, 4.0, 3.0], 2: [2.0, 5.0]}
# movie_rating::{1: [3.0], 3: [3.0], 2: [4.0], 5: [5.0], 4: [2.0]}
# terms=['joker', 'superhero', 'batman', 'gotham', 'dark', 'returns', 'knight', 'robin']
# term_movie=
# {'dark': set([2, 3]), 'superhero': set([1, 5]), 'batman': set([1, 2, 4, 5]), 'returns': set([3]), 'joker': set([4]), 'gotham': set([4]), 'knight': set([2, 3]), 'robin': set([1])}
# movie_meta = {1: {'superhero': 1, 'batman': 1, 'robin': 1}, 2: {'knight': 1, 'batman': 1, 'dark': 1}, 3: {'knight': 1, 'dark': 1, 'returns': 1}, 4: {'gotham': 1, 'batman': 1, 'joker': 1}, 5: {'superhero': 1, 'batman': 1}}


def bm(m):  # movie_id is set, find all the rating for that movie
    m_rating = movie_rating[m]
    res = np.sum(np.array(m_rating)-avg_rating)/len(m_rating)
    bm_dict[m] = res
    # print (bm_dict)
    # print (res)
    # print (m)
    return res


def b(target_movie_id, target_user_id):
    if target_movie_id in bm_dict:
        b_m = bm_dict[target_movie_id]
    else:
        b_m = bm(target_movie_id)
    # b_m = bm(target_movie_id) #-1.4
    movie_list = user_movie[target_user_id]
    up = []
    up = 0
    for m in movie_list:
        if m in bm_dict:
            tmp = bm_dict[m]
        else:
            tmp = bm(m)
        # print (tmp)
        # print (bm(m))
        up += um_rating[(target_user_id, m)]-avg_rating-tmp
    b_u = up/len(user_rating[target_user_id])
    return avg_rating+b_u+b_m


prefix = b(target_movie_id, target_user_id)  # 2.0
print(prefix)


def d(m):
    tf = np.zeros(term_num)
    idf = np.zeros(term_num)
    t = movie_meta[m].keys()
    total_term_num = sum(movie_meta[m].values())
    for i in t:
        tf[term_index[i]] = movie_meta[m][i]/total_term_num
        idf[term_index[i]] = math.log(movie_num / len(term_movie[i]))
    tmp = np.array(tf)*np.array(idf)
    return tmp.tolist()


s_list = []
d_target = d(target_movie_id)

for j in R_u:
    s_list.append(1 - spatial.distance.cosine(d_target, d(j)))

up = []
for j in range(len(R_u)):
    r_uj = um_rating[(target_user_id, R_u[j])]
    b_uj = b(R_u[j], target_user_id)
    up.append(s_list[j]*(r_uj-b_uj))

suffix = np.sum(up)/np.sum(s_list)

res = prefix+suffix
print(round(res, 1))
