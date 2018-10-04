import sys


def main():

    # read in data
    hubs = {}
    auths = {}

    # initial score
    hub_scores = {}
    auth_scores = {}

    num_of_links = sys.stdin.readline()
    line = sys.stdin.readline()
    while line:
        line_array = line.split(",")
        line_array = [int(i) for i in line_array]

        if line_array[0] in hubs:
            hubs[line_array[0]].append(line_array[1])
        else:
            hubs[line_array[0]] = [line_array[1]]

        hub_scores[line_array[0]] = 1

        if line_array[1] in auths:
            auths[line_array[1]].append(line_array[0])
        else:
            auths[line_array[1]] = [line_array[0]]

        auth_scores[line_array[1]] = 1

        try:
            line = sys.stdin.readline()
        except:
            break

    for iter in range(10):
        # update auths scores
        for auth_i, hub_i in auths.items():
            new_auth_scores = 0
            for hub_of_auth_i in hub_i:
                new_auth_scores += hub_scores[hub_of_auth_i]
            auth_scores[auth_i] = new_auth_scores

        for hub_i, auth_i in hubs.items():
            new_hub_scores = 0
            for auth_of_hub_i in auth_i:
                new_hub_scores += auth_scores[auth_of_hub_i]
            hub_scores[hub_i] = new_hub_scores

    sorted_hubs = []
    sorted_auths = []

    for hub in hub_scores:
        sorted_hubs.append([hub, hub_scores[hub]])

    for auth in auth_scores:
        sorted_auths.append([auth, auth_scores[auth]])

    sorted_auths.sort(key=lambda sl: (-sl[1], sl[0]))
    sorted_hubs.sort(key=lambda sl: (-sl[1], sl[0]))

    result_hubs = []
    result_auths = []
    for i in range(3):
        result_hubs.append(str(sorted_hubs[i][0]))
    for i in range(3):
        result_auths.append(str(sorted_auths[i][0]))

    print(",".join(result_hubs))
    print(",".join(result_auths))


if __name__ == '__main__':
    main()
