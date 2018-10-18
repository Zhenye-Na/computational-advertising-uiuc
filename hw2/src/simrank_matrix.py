from collections import defaultdict
from scipy.sparse import csr_matrix, csc_matrix, diags
import numpy as np

C = 0.8
line_1, line_2, line_3, line_4, line_5, line_6 = [], [], [], [], [], []
cnt = int(raw_input().strip())
user_dict = defaultdict(list)
ad_dict = defaultdict(list)
for _ in range(cnt):
    item_list = list(raw_input().split(','))
    user_dict[int(item_list[0])].append(int(item_list[1]))
    ad_dict[int(item_list[1])].append(int(item_list[0]))
target_list = list(raw_input().split(','))
user = int(target_list[0])
ad = int(target_list[1])
users = list(user_dict.keys())
users.sort()
ads = list(ad_dict.keys())
ads.sort()
ads_m = np.matrix(np.identity(len(ads)))
graph = np.matrix(np.zeros([len(users), len(ads)]))
for key, value in user_dict.items():
    for v in value:
        graph[users.index(key), ads.index(v)] = 1


def sort_inorder(tt_list, res_list, tt):
    ind = np.argpartition(tt_list, 1)[0]
    res_list.append(str(tt[ind]))
    tt_list[ind] = 1


def evident_calc(flag, tt, ua):
    return np.multiply(1 - np.power(0.5, ua), tt) if flag else np.multiply(1 - np.exp(-ua), tt)


def simple_simrank(N):
    update_usr = diags(np.ones(len(users)))
    update_ads = diags(np.ones(len(ads)))
    pref_user = np.dot(graph.sum(axis=1), graph.sum(axis=1).T)
    pref_ad = np.dot(graph.sum(axis=0).T, graph.sum(axis=0))

    for _ in range(N):
        temp = (graph*update_ads*graph.T)*C/pref_user
        update_usr = temp - np.diag(np.diag(temp)) + diags(np.ones(len(users)))
        temp = graph.T*update_usr*graph*C/pref_ad
        update_ads = temp - np.diag(np.diag(temp)) + diags(np.ones(len(ads)))
    return update_usr, update_ads


def e_inco_simrank(update_usr, update_ads):

    tar_usr_simple = -update_usr[users.index(user)].A1
    tar_ad_simple = -update_ads[ads.index(ad)].A1
    tar_usr_simple[users.index(user)] = 1
    tar_ad_simple[ads.index(ad)] = 1
    common_user = (graph*graph.T[:, users.index(user)]).T.A[0]
    common_ad = (graph.T * graph[:, ads.index(ad)]).T.A[0]

    geo_user = evident_calc(1, tar_usr_simple, common_user)
    geo_ad = evident_calc(0, tar_ad_simple, common_ad)
    exp_user = evident_calc(1, tar_usr_simple, common_user)
    exp_ad = evident_calc(0, tar_ad_simple, common_ad)
    return tar_usr_simple, tar_ad_simple, geo_user, geo_ad, exp_user, exp_ad


def simrank():
    update_usr, update_ads = simple_simrank(10)
    tar_usr_simple, tar_ad_simple, geo_user, geo_ad, exp_user, exp_ad = e_inco_simrank(
        update_usr, update_ads)

    for _ in range(3):
        sort_inorder(tar_usr_simple, line_1, users)
        sort_inorder(tar_ad_simple, line_2, ads)
        sort_inorder(geo_user, line_3, users)
        sort_inorder(geo_ad, line_4, ads)
        sort_inorder(exp_user, line_5, users)
        sort_inorder(exp_ad, line_6, ads)


if __name__ == "__main__":
    simrank()

    print ','.join(line_1)
    print ','.join(line_2)
    print ','.join(line_3)
    print ','.join(line_4)
    print ','.join(line_5)
    print ','.join(line_6)
