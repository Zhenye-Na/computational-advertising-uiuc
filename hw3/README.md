# Recommender Systems

## Problem

The problem statement is given in this Assignment File which has been attached in Wiki.

### Input Format

The input contains the (user,movie) rating information, movie metadata and the (user,movie) pair for which you need to estimate the rating.

The first line of the input contains 2 space seperated integers R M. R is the number of lines of rating information. M is the number of movies.

Next R lines contain the rating information. Each line will contain 3 space seperated values (user id, movie id, rating).

Next M lines contain the metadata information. The first word/value of each line is the movie id. The rest of the words are the metadata information about that movie.

The last line with contain 2 space seperated integers (target user id, target movie id) for which you need to estimate the rating.

Please refer to the sample input 0 below.

There are 5 rating information lines and 5 movie metadata lines. You need to find the rating that user 1 would have given to movie 4.

### Constraints

NA

### Output Format

Your ouput should be a single floating point value for the estimated rating. Round the output to 1 decimal point.

#### Sample Input 0

```
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
```

#### Sample Output 0

```
2.0
```

#### Sample Input 1

```
6 5
1 1 3.0
1 2 4.0
1 3 3.0
2 1 2.8
2 4 2.0
2 5 5.0
1 batman robin superhero
2 batman dark knight
3 dark knight returns
4 batman joker gotham
5 batman superhero
1 5
```

#### Sample Output 1

```
5.1
```