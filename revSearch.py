import requests
import json

textEngineURL = "https://www.googleapis.com/customsearch/v1"
searchKey = "AIzaSyAmrHH4531VU8H1KV5C32sqHI1HIV_L-dc"
textSearchCX = "016220867362134571083:ntcgj0p32rg"


def reverseSearchText(audioTextChunks):
    textPieces = []
    audioChunksTemp = []
    for audioText in audioTextChunks:
        audioChunksTemp.append(' '.join([audioText, "what show"]))
        audioChunksTemp.append(' '.join([audioText, "what movie"]))

    audioTextChunks = audioChunksTemp

    for text in audioTextChunks:
        response = requests.get(textEngineURL, params={"key":searchKey, "cx":textSearchCX, "q":text})
        entries = response.json()['items']
        entries = [[entry['title'], entry['snippet']] for entry in entries]
        entries = entries[:5]
        for entry in entries:
            textPieces.append(entry[0].replace('\n', ''))
            textPieces.append(entry[1].replace('\n', ''))
    print(' '.join(textPieces))
    return ' '.join(textPieces)
