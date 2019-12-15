
import boto3
#import json
import sys

def OCRFrame(frame): 
    client=boto3.client('rekognition')
    with open(frame, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    textDetections=response['TextDetections']
    print ('Detected text')
    combinedText = []
    for text in textDetections:
        print ('Detected text:' + text['DetectedText'])
        print ('Confidence: ', text['Confidence'])
        # print ('Id: {}'.format(text['Id']))
        # if 'ParentId' in text:
        #     print ('Parent Id: {}'.format(text['ParentId']))
        print ('Type:' + text['Type'])
        if text['Confidence'] > 85 and text['Type'] == 'WORD':
            combinedText.append(text['DetectedText'])
    return ' '.join(combinedText)

if __name__ == "__main__":
    framePath=sys.argv[1]
    print(OCRFrame(framePath))
        

