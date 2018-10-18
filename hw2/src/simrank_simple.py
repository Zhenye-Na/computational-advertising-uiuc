import math

users = {}
ads = {}
user_sim = {}
ad_sim = {}
C = 0.8
iterations = 10


line_index = 0
linelim = 1

while line_index < linelim:
    line = input()
    if line_index == 0 or line_index == linelim - 1:
        # print(line)
        if line_index == 0:
            linelim = int(line.split("\n")[0]) + 2
            # print(linelim)
        if line_index == linelim - 1:
            line = line.split(",")
            u1 = line[0]
            m1 = line[1]
        line_index += 1
        continue
    line = line.split("\n")[0].split(",")
    if line[0] not in users:
        users[line[0]] = []
    users[line[0]].append(line[1])
    if line[1] not in ads:
        ads[line[1]] = []
    ads[line[1]].append(line[0])
    line_index += 1


for user in users:
    user_sim[user] = {}
    for user2 in users:
        user_sim[user][user2] = 0.0
    user_sim[user][user] = 1.0

for ad in ads:
    ad_sim[ad] = {}
    for ad2 in ads:
        ad_sim[ad][ad2] = 0.0
    ad_sim[ad][ad] = 1.0

for iteration in range(iterations):
    for user in users:
        for user2 in users:
            if user2 == user:
                continue
            total = 0.0
            for ad in users[user]:
                for ad2 in users[user2]:
                    total += ad_sim[ad][ad2]
            user_sim[user][user2] = (
                C * total) / (len(users[user]) * len(users[user2]))

    for ad in ads:
        for ad2 in ads:
            if ad == ad2:
                continue
            total = 0.0
            for user in ads[ad]:
                for user2 in ads[ad2]:
                    total += user_sim[user][user2]
            ad_sim[ad][ad2] = (C * total) / (len(ads[ad]) * len(ads[ad2]))


top_users = sorted(user_sim[u1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)
top_ads = sorted(ad_sim[m1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)

print(",".join([t[0] for t in top_users[1:4]]))
print(",".join([t[0] for t in top_ads[1:4]]))


# With geometric evidence
for user in users:
    for user2 in users:
        if user2 == user:
            continue
        common = len(list(set(users[user]) & set(users[user2])))
        evidence = 0.0
        for i in range(common):
            evidence += 1.0 / (2**(i + 1))
        user_sim[user][user2] *= evidence

for ad in ads:
    for ad2 in ads:
        if ad == ad2:
            continue
        common = len(list(set(ads[ad]) & set(ads[ad2])))
        evidence = 0.0
        for i in range(common):
            evidence += 1.0 / (2**(i + 1))
        ad_sim[ad][ad2] *= evidence


top_users = sorted(user_sim[u1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)
top_ads = sorted(ad_sim[m1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)

print(",".join([t[0] for t in top_users[1:4]]))
print(",".join([t[0] for t in top_ads[1:4]]))


# With exponential evidence
for user in users:
    for user2 in users:
        if user2 == user:
            continue
        common = len(list(set(users[user]) & set(users[user2])))
        evidence = 0.0
        for i in range(common):
            evidence += 1.0 / (2**(i + 1))
        if evidence > 0.0:
            user_sim[user][user2] /= evidence
        evidence = 1.0 - math.exp(-common)
        user_sim[user][user2] *= evidence

for ad in ads:
    for ad2 in ads:
        if ad == ad2:
            continue
        common = len(list(set(ads[ad]) & set(ads[ad2])))
        evidence = 0.0
        for i in range(common):
            evidence += 1.0 / (2**(i + 1))
        if evidence > 0.0:
            ad_sim[ad][ad2] /= evidence
        evidence = 1.0 - math.exp(-common)
        ad_sim[ad][ad2] *= evidence


top_users = sorted(user_sim[u1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)
top_ads = sorted(ad_sim[m1].items(), key=lambda t: (
    float(t[1]), -float(t[0])), reverse=True)
print(",".join([t[0] for t in top_users[1:4]]))
print(",".join([t[0] for t in top_ads[1:4]]))
