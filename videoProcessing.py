import cv2
import subprocess
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

"""
 videoPath: path to video
 return: string of audio in video
"""
# def getAudioText(audioPath):
#     # Instantiates a client
#     client = speech.SpeechClient()

#     # Loads the audio into memory
#     with io.open(audioPath, 'rb') as audio_file:
#         content = audio_file.read()
#         audio = types.RecognitionAudio(content=content)

#     config = types.RecognitionConfig(
#         encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=44100,
#         language_code='en-US')

#     # Detects speech in the audio file
#     response = client.recognize(config, audio)

#     audioLines = [result.alternatives[0].transcript for result in response.results]
#     print(audioLines)
#     return audioLines



# def getAudio(videoPath):
#     command = "ffmpeg -i {} -ab 160k -ac 1 -ar 44100 -vn {}.wav".format(videoPath, videoPath[:-4])
#     subprocess.call(command, shell=True)

    # return ''.join([videoPath[:-4], ".wav"])

def getFrames(dirname, videoPath):
    vidObj = cv2.VideoCapture(videoPath)
    framePaths = []

    currentFrameNo = 0
    success = True
    frameRate = vidObj.get(cv2.CAP_PROP_FPS)
    totalFrames = vidObj.get(cv2.CAP_PROP_FRAME_COUNT)
    frameCount = 0

    while success and currentFrameNo < totalFrames:
        # read from currentFrameNo
        vidObj.set(cv2.CAP_PROP_POS_FRAMES, currentFrameNo)

        success, image = vidObj.read()

        if not success:
             continue
             
        framePath = "/".join([dirname, "frame{0}.jpg".format(frameCount)])

        print("Saving to ", framePath)
        print("\n\n\n\n\n\n\n\n")
        cv2.imwrite(framePath, image)
        framePaths.append(framePath)
        frameCount += 1
        currentFrameNo += frameRate

    print("Returning from getFrames", len(framePaths))
    return framePaths
