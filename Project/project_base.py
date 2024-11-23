import shutil
import os
import kagglehub
import tqdm


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nrclex import NRCLex

nltk.download('punkt')
nltk.download('stopwords') 
nltk.download('averaged_perceptron_tagger')  

current_directory = os.getcwd()

csv_path = r"C:\Users\kakao\Desktop\Ajou_SocialNetworkAnalysis\Project\song-lyrics-dataset\csv"

artists = os.listdir(csv_path)
for artist in artists:
    lyrics_data = os.path.join(csv_path,artist)
    print(lyrics_data)
    df1 = pd.read_csv(lyrics_data)

# 1. Knowledge-based method

# VADER 감성 분석기 초기화
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']  # 전체적인 감정 점수 (-1~1)
    # 긍정, 부정, 중립으로 분류
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_emotions(text):
    emotions = NRCLex(text).raw_emotion_scores
    # 감정이 없는 경우 0으로 채움
    for emotion in ['joy', 'sadness', 'anger', 'fear', 'anticipation', 'trust', 'surprise', 'disgust']:
        if emotion not in emotions:
            emotions[emotion] = 0
    return emotions

def dominant_emotion(emotion_scores):
    return max(emotion_scores, key=emotion_scores.get)

df1['Lyric'] = df1['Lyric'].apply(str)
df1['Sentiment'] = df1['Lyric'].apply(analyze_sentiment)
df1['Compound Score'] = df1['Lyric'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

df1['Emotion Scores'] = df1['Lyric'].apply(analyze_emotions)
df1['Dominant Emotion'] = df1['Emotion Scores'].apply(dominant_emotion)

print(df1.head())
df1.to_csv("./emotion_lyric/Taylor_Swift.csv")

# 테일러 스위프트 노래별 가사를 emotion 분석한 결과를 .csv로 저장함

