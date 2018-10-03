# Implement SimRank and SimRank with evidence


## Problem

In this question, you are required to implement the SimRank algorithm and SimRank with 2 forms of evidence weights with a supported programming language of your choice. In each case, your iterations must begin with user updates, alternating with ad similarity updates. We will use this [reference](https:arxiv.org/pdf/0712.0499.pdf) for the algorithm details. You can use the sample test case to debug your code, however the final test case is significantly larger and hence may require an efficient implementation. You must keep this in mind when you make your submission. Remember to use [partial sum sharing](https://en.wikipedia.org/wiki/SimRank) in your implementation.

### Input Format

The input consits of **weighted User-Ad links**. 

The first line specifies the total number of links `N`, followed by `N` lines each containing **3** comma separated entries - `U`, `A`, `S` where `U` and `A` are integers representing **User** and **Ad Ids**, `0 <= U <= 1,000,000` and `0 <= A <= 1,000,000`, and **score** `S` is a *float* score value for that link, `0.0 <= S <= 1,000.0`. The score is based on how fast the user responded to the Ad (a higher score denotes a greater proclivity).

This is then followed by a single line with **2 ids**, `Q_U` and `Q_A`. You need to output the **3** most similar users to `Q_U` and the **3** most similar ads to `Q_A` with each of the variations of simrank. In case 2 of the 3 entries have the same similarity score in any case, use the same tiebreak criterion as in the previous assignment.

A sample input looks like 

```
N
U1, A1, S1
U2, A2, S2
...
UN, AN, SN
Q_U,Q_A
```

Note `U1` is a user-id, while `A1` is the advertisement-id for a specific display-ad clicked by `U` and `S1` is the link weight. Note that a given user can click more than one ad, meaning multiple lines could have the same user-id, but no two lines are identical. You are required to build the bipartitle weighted User-Ad graph using the above links.

### Task One - Simple SimRank iterations

**Implement conventional SimRank and compute the similarities of users to each other and ads to other ads**. You need to use the partial sums trick described in the links provided with the assignment description in your implementation. Initialize the algorithm with the usual procedure (similarity of a node to itself is 1 and 0 to all others), and perform K=10 iterations of User and Ad-similarity updates (start with user similarity updates). The constants C1 and C2 are both set to 0.8. Let us call the similarity scores obtained after K=10 iterations simple\_simrank\_scores.

### Task Two - Incorporate evidence

In section 7 of the reference, two forms are introduced for evidence scores (geometric in eq 7.3 and exponential in eq 7.4). **You will apply each of these forms to the results obtained after 10 iterations of Simple SimRank and obtain the new similarity scores for users and ads**. Let us call these 2 new sets of scores evidence\_geometric\_scores and evidence\_exponential\_scores.


You output should contain 6 lines:

- Line 1 - 3 most similar users to `Q_U` with simple\_simrank\_scores
- Line 2 - 3 most similar ads to `Q_A` with simple\_simrank\_scores
- Line 3 - 3 most similar users to `Q_U` with evidence\_geometric\_scores
- Line 4 - 3 most similar ads to `Q_A` with evidence\_geometric\_scores
- Line 5 - 3 most similar users to `Q_U` with evidence\_exponential\_scores
- Line 6 - 3 most similar ads to `Q_A` with evidence\_exponential\_scores

### Constraints

- No constraints.

### Output Format

Your output must contain 6 lines as described above, follow the same instructions as the last assignment for tie-breaks.

A sample output looks like this:

```
U_1,U_2,U_3
A_1,A_2,A_3
U_4,U_5,U_6
A_4,A_5,A_6
U_7,U_8,U_9
A_7,A_8,A_9
```


**Sample Input 0**

```
8
1,20,1.0
2,20,2.0
2,38,2.5
3,20,1.2
3,38,1.7
4,38,2.5
5,1235,0.9
5,8271,3.8
1,20
```

**Sample Output 0**

```
2,3,4
38,1235,8271
2,3,4
38,1235,8271
2,3,4
38,1235,8271
```

**Explanation 0**

In this sample case the results are the same with and without evidence.