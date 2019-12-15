import json
from collections import Counter

'''
 celebs: list of strings (celeb names)
 return: list of 5 strings (top guesses)
'''
def getGuessesFromCelebs(celebs):
    json_file = open('actorsToMovies.json')
    json_str = json_file.read()
    actorsToMovies = json.loads(json_str)

    movies = Counter()
    print("!", celebs)
    for celeb in celebs:
        if celeb[0] in actorsToMovies:
            for movie in actorsToMovies[celeb[0]]:
                movies[movie]+=celeb[1]
    print(movies.most_common(5))
    return movies.most_common(5)

def bruteForce(text):
    json_file = open('movies.json')
    json_str = json_file.read()
    movies = json.loads(json_str)

    movieCounter = Counter()
    for movie in movies:
        count = text.count(movie)
        if count > 0:
            movieCounter[movie] += count

    return movieCounter
