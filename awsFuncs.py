import boto3
"""
framePath: path to frame image
return: list of 3-tuples of the form (celebrity Name, Confidence, URL)
obtain list of all the celebrities in the frame with the confidence level
"""
def getCelebsFromFrame(frame):
    client=boto3.client('rekognition')
    with open(frame, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})
    celebs=[]
    for celebrity in response['CelebrityFaces']:
        if len(celebrity['Urls']) > 0 and 'imdb' in celebrity['Urls'][0]:
            url = celebrity['Urls'][0]
        else:
            url = None
        celebs.append( (celebrity['Name'], celebrity['MatchConfidence'], url) )
    print(celebs)
    return celebs

"""
frame: path to jpg or png screencap
return: string of text in the image (or a list if necessary)
analyze frame and retrieve all relevant text from it
"""
def getTextFromFrame(frame):
    client=boto3.client('rekognition')
    with open(frame, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    textDetections=response['TextDetections']
    combinedText = []
    for text in textDetections:
        #print ('Detected text:' + text['DetectedText'])
        #print ('Confidence: ', text['Confidence'])
        #print ('Type:' + text['Type'])
        if text['Confidence'] > 85 and text['Type'] == 'WORD':
            combinedText.append(text['DetectedText'])
    return ' '.join(combinedText)
