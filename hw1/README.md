# Implement the HITS algorithm

## Problem

In this question, you are required to implement the HITS algorithm with a supported programming language of your choice. You must follow the initialization, normalization and iteration procedure specified in this reference (refer to page 403). You can use the sample test cases to debug your code, however the final test case is significantly larger and hence may require an efficient implementation. You must keep this in mind when you make your submission.

### Input Format

The input consits of User-Movie links, where users denote the hubs and movies denote the authorities in the **HITS algorithm**. 

The first line specifies the total number of links N, followed by N lines each containing 2 comma separated non-negative integer values - U, M where `0 <= U <= 1,000,000` and `0 <= M <= 1,000,000` 
A sample input looks like 

```
N
U1, M1
U2, M2
...
UN, MN
```


Note `U1` is a user-id, while `M1` is the movie-id for a movie reviewed positively by `U`. Note that a given user can review more than one movie, meaning multiple lines could have the same user-id, but no two lines are identical.

You are required to build the bipartitle Hub-Authority graph (with users as hubs, and movies as authorities) using the above links, initialize the algorithm with equal weights assigned to all hubs and authorities, and perform K=10 iterations of Authority and Hub-Score updates.

### Constraints

No constraints.

### Output Format

Your output must contain 2 lines, 
The first line contains the comma separated IDs of the top 3 hubs (by their hub-score) in decreasing order meaning that the first ID corresponds to the highest score. Note that the top hubs are the most profilic movie reviewers. 

In case there is a tie, print the smaller ID value first (i.e. if ID's 1 and 2 are both tied for first place, then the first place will be assigned to ID 1 and second place to ID 2). 

The second line contains the comma separated IDs of the top 3 authorities (by authority-score), which in this case refers to critically acclaimed movies. Follow the same instructions as above for the order of IDs and tie-breaking. 

A sample output looks like this-

```
U1,U2,U3
M1,M2,M3
```


**Sample Input 0**

```
4
1,1
2,2
3,3
4,4
```

**Sample Output 0**

```
1,2,3
1,2,3
```

**Explanation 0**

Each user receives the same hub-score after K=10 iterations, thus they are sorted to place the smaller ID first. Same for the movies.

**Sample Input 1**

```
6
2100,10897
2100,21443
12,10897
12,21443
12,38976
387,41005
```

**Sample Output 1**

````
12,2100,387
10897,21443,38976
```