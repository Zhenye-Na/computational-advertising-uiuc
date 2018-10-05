"""
Implementation of SimRank algorithm.

ref: https://en.wikipedia.org/wiki/SimRank

@date: Oct 4, 2018
@author: Zhenye Na
"""

import sys
import numpy
from numpy import matrix


num_of_links = int(sys.stdin.readline())

logs = []

for _ in range(num_of_links):
    log = sys.stdin.readline().strip()
    logs.append(log)

query = sys.stdin.readline().strip().split(",")
query_user = query[0]
query_ad = query[1]


logs_tuple = [tuple(log.split(",")) for log in logs]

queries = list(set([ log[0] for log in logs_tuple ]))
ads = list(set([ log[1] for log in logs_tuple ]))
weights = list(set([ log[2] for log in logs_tuple ]))

# Graph means the relations number
graph = numpy.matrix(numpy.zeros([len(queries), len(ads)]))

# create graph
for log in logs_tuple:
    query = log[0]
    ad = log[1]
    q_i = queries.index(query)
    a_j = ads.index(ad)
    graph[q_i, a_j] += 1

# similarity scores
query_sim = matrix(numpy.identity(len(queries)))
ad_sim = matrix(numpy.identity(len(ads)))


def get_ads_num(query):
    q_i = queries.index(query)
    return graph[q_i]


def get_queries_num(ad):
    a_j = ads.index(ad)
    return graph.transpose()[a_j]


def get_ads(query):
    series = get_ads_num(query).tolist()[0]
    return [ ads[x] for x in range(len(series)) if series[x] > 0 ]


def get_queries(ad):
    series = get_queries_num(ad).tolist()[0]
    return [ queries[x] for x in range(len(series)) if series[x] > 0 ]


def query_simrank(q1, q2, C):
    if q1 == q2:
        return 1

    prefix = C / (get_ads_num(q1).sum() * get_ads_num(q2).sum())
    postfix = 0

    for ad_i in get_ads(q1):
        for ad_j in get_ads(q2):
            i = ads.index(ad_i)
            j = ads.index(ad_j)
            postfix += ad_sim[i, j]

    return prefix * postfix


def ad_simrank(a1, a2, C):
    if a1 == a2:
        return 1

    prefix = C / (get_queries_num(a1).sum() * get_queries_num(a2).sum())
    postfix = 0

    for query_i in get_queries(a1):
        for query_j in get_queries(a2):
            i = queries.index(query_i)
            j = queries.index(query_j)
            postfix += query_sim[i,j]

    return prefix * postfix


def simple_simrank(C=0.8, k=10):
    """Simple SimRank iterations."""
    for _ in range(k):
        # queries simrank
        new_query_sim = matrix(numpy.identity(len(queries)))
        for qi in queries:
            for qj in queries:
                i = queries.index(qi)
                j = queries.index(qj)
                new_query_sim[i,j] = query_simrank(qi, qj, C)

        # ads simrank
        new_ad_sim = matrix(numpy.identity(len(ads)))
        for ai in ads:
            for aj in ads:
                i = ads.index(ai)
                j = ads.index(aj)
                new_ad_sim[i,j] = ad_simrank(ai, aj, C)

        query_sim = new_query_sim
        ad_sim = new_ad_sim

    return query_sim, ad_sim


def query_simrank_geometric(q1, q2):
    if q1 == q2:
        return 1

    prefix = 0.
    num = numpy.sum(get_ads_num(q1) == get_ads_num(q2))
    for i in range(1, num+1):
        prefix += 1 / (2 ** i)

    postfix = 0

    for ad_i in get_ads(q1):
        for ad_j in get_ads(q2):
            i = ads.index(ad_i)
            j = ads.index(ad_j)
            postfix += ad_sim[i, j]

    return prefix * postfix


def ad_simrank_geometric(a1, a2):
    if a1 == a2:
        return 1

    prefix = 0.
    num = numpy.sum(get_queries_num(a1) == get_queries_num(a2))
    for i in range(1, num+1):
        prefix += 1 / (2 ** i)
    postfix = 0

    for query_i in get_queries(a1):
        for query_j in get_queries(a2):
            i = queries.index(query_i)
            j = queries.index(query_j)
            postfix += query_sim[i,j]

    return prefix * postfix


def evidence_geometric(k=10):
    """Incorporate evidence - geometric."""
    for _ in range(k):
        # queries simrank
        new_query_sim = matrix(numpy.identity(len(queries)))
        for qi in queries:
            for qj in queries:
                i = queries.index(qi)
                j = queries.index(qj)
                new_query_sim[i,j] = query_simrank_geometric(qi, qj)

        # ads simrank
        new_ad_sim = matrix(numpy.identity(len(ads)))
        for ai in ads:
            for aj in ads:
                i = ads.index(ai)
                j = ads.index(aj)
                new_ad_sim[i,j] = ad_simrank_geometric(ai, aj)

        query_sim = new_query_sim
        ad_sim = new_ad_sim

    return query_sim, ad_sim



def evidence_exponential():
    """Incorporate evidence - exponential."""
    pass


def print_result_simple_simrank(query_user, query_ad):
    # for query
    q_i = queries.index(query_user)
    a_j = ads.index(query_ad)

    query_sim_list = query_sim.tolist()
    ad_sim_list = ad_sim.tolist()

    target_query_list = query_sim_list[q_i]
    target_ad_list = ad_sim_list[a_j]

    queries_int = [int(i) for i in queries]
    query_list = list(zip(target_query_list, queries_int))

    ads_int = [int(i) for i in ads]
    ad_list = list(zip(target_ad_list, ads_int))

    query_list.sort(key=lambda sl: (-sl[0], sl[1]))
    ad_list.sort(key=lambda sl: (-sl[0], sl[1]))


    q_result = []
    for i in range(1, 4):
        q_result.append(str(query_list[i][1]))

    a_result = []
    for i in range(1, 4):
        a_result.append(str(ad_list[i][1]))

    print(",".join(q_result))
    print(",".join(a_result))


if __name__ == '__main__':
    # print(queries)
    # print(ads)
    query_sim, ad_sim = simple_simrank()
    print_result_simple_simrank(query_user, query_ad, query_sim, ad_sim)
    # print(query_sim)
    # print(ad_sim)
    query_sim, ad_sim = evidence_geometric()
    print_result_simple_simrank(query_user, query_ad, query_sim, ad_sim)
