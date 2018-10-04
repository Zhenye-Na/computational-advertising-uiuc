"""
Implementation of SimRank algorithm.

ref: https://en.wikipedia.org/wiki/SimRank

@date: Oct 4, 2018
@author: Zhenye Na
"""

import sys

k = 10
c1 = c2 = 0.8

def simple_simrank(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad):
    """
    Simple SimRank iterations.

    Args:
        users
        ads
        users_sim_scores
        ads_sim_scores
        users_partial_sum
        ads_partial_sum
        query_user
        query_ad
    """
    # memoization for ads partial sum
    for users_key, users_score_val in users_sim_scores.items():
        users_key_array = users_key.split(",")
        users_key_array = [float(i) for i in users_key_array]

        for q_prime_neighbors in users[users_key_array[1]]:
            similarity_score = 0.
            for q_neighbors in users[users_key_array[0]]:
                similarity_score += ads_sim_scores["{},{}".format(q_neighbors, q_prime_neighbors)]
            ads_partial_sum[q_prime_neighbors] = similarity_score

    # memoization for users partial sum
    for ads_key, ads_score_val in ads_sim_scores.items():
        ads_key_array = ads_key.split(",")
        ads_key_array = [float(i) for i in ads_key_array]

        for a_prime_neighbors in ads[ads_key_array[1]]:
            similarity_score = 0.
            for a_neighbors in ads[ads_key_array[0]]:
                similarity_score += users_sim_scores["{},{}".format(a_neighbors, a_prime_neighbors)]
            users_partial_sum[a_prime_neighbors] = similarity_score


    for i in range(k):
        # Eq. 4.1
        for users_key, users_score_val in users_sim_scores.items():
            users_key_array = users_key.split(",")
            users_key_array = [float(i) for i in users_key_array]

            factor = c1 / (len(users[users_key_array[0]]) * len(users[users_key_array[1]]))

            new_sim_score = 0.
            for q_prime_neighbors in users[users_key_array[1]]:
                new_sim_score += ads_partial_sum[q_prime_neighbors]

            users_sim_scores["{},{}".format(users_key_array[0], users_key_array[1])] = factor * new_sim_score

        # Eq. 4.2
        for ads_key, ads_score_val in ads_sim_scores.items():
            ads_key_array = ads_key.split(",")
            ads_key_array = [int(i) for i in ads_key_array]

            factor = c2 / (len(ads[ads_key_array[0]]) * len(ads[ads_key_array[1]]))

            new_sim_score = 0.
            for a_prime_neighbors in ads[ads_key_array[1]]:
                new_sim_score += users_partial_sum[a_prime_neighbors]

            ads_sim_scores["{},{}".format(ads_key_array[0], ads_key_array[1])] = factor * new_sim_score


    query_user_neighbors = users[query_user]
    user_rank = []
    for neighbor in query_user_neighbors:
        user_rank.append(neighbor, users_sim_scores["{},{}".format(query_user, neighbor)])

    user_rank.sort(key=lambda sl: (-sl[1], sl[0]))

    user_result = []
    for i in range(3):
        user_result.append(str(user_rank[i][0]))

        print(",".join(user_result))



def evidence_geometric():
    """Incorporate evidence - geometric."""
    pass



def evidence_exponential():
    """Incorporate evidence - exponential."""
    pass


def main(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad):
    """
    Pipleline of SimRank algorithm.

    Args:
        users
        ads
        users_sim_scores
        ads_sim_scores
        users_partial_sum
        ads_partial_sum

    """
    simple_simrank(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad)
    evidence_geometric(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad)
    evidence_exponential(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad)


if __name__ == '__main__':
    num_of_links = int(sys.stdin.readline())

    # dictionary of users, mapping from users to ads
    users = {}

    # dictionary of ads, mapping from ads to users
    ads = {}

    # dictionary of weights, link weights
    weights = {}

    # similarity scores for users
    users_sim_scores = {}

    # similarity scores for ads
    ads_sim_scores = {}

    # partial sum memoization for users
    users_partial_sum = {}

    # partial sum memoization for ads
    ads_partial_sum = {}

    for _ in range(num_of_links):
        line = sys.stdin.readline().split(",")
        line_array = [float(i) for i in line]

        if line_array[0] in users:
            users[line_array[0]].append(line_array[1])
        else:
            users[line_array[0]] = [line_array[1]]

        users_sim_scores["{},{}".format(line_array[0], line_array[0])] = 1.
        users_sim_scores["{},{}".format(line_array[0], line_array[1])] = 0.
        users_sim_scores["{},{}".format(line_array[1], line_array[0])] = 0.

        if line_array[1] in ads:
            ads[line_array[1]].append(line_array[0])
        else:
            ads[line_array[1]] = [line_array[0]]

        ads_sim_scores["{},{}".format(line_array[1], line_array[1])] = 1.
        ads_sim_scores["{},{}".format(line_array[1], line_array[0])] = 0.
        ads_sim_scores["{},{}".format(line_array[0], line_array[1])] = 0.

        weights["{},{}".format(line_array[0], line_array[1])] = line_array[2]


    # query user and ad
    line = sys.stdin.readline().split(",")
    line_array = [int(i) for i in line]
    query_user = line_array[0]
    query_ad = line_array[1]


    main(users, ads, users_sim_scores, ads_sim_scores, users_partial_sum, ads_partial_sum, query_user, query_ad)
