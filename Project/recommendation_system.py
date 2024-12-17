import pandas as pd
import numpy as np
from pathlib import Path

# 상대 경로 설정
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "database" / "song_lyric_sentiment_result.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(file_path)
    print("Data Loaded Successfully!")
except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.")
    exit()

# NRC_emotion_vector_norm 전처리 함수
def preprocess_emotion_vectors(vector_str):
    """
    Preprocess NRC_emotion_vector_norm strings:
    - Ensure the string format is converted to a list of floats.
    - Handle missing or corrupted data.
    """
    try:
        if pd.isna(vector_str):
            return [0.0] * 8  # 결측값을 기본값으로 채움
        # 숫자들 사이에 공백만 있는 경우, 쉼표로 변환
        # cleaned_str = vector_str.strip().replace(" ", ",")
        # return list(map(float, cleaned_str.strip("[]").split(",")))
        cleaned_str = vector_str.replace("[","").replace("]","").split()
        cleaned_str = list(map(float,cleaned_str))
        return cleaned_str
    except Exception as e:
        print(f"Error processing vector: {vector_str}, Error: {e}")
        return [0.0] * 8  # 오류 발생 시 기본값 반환

# NRC_emotion_vector_norm 전처리

df["vader_sentiment"] = df["vader_sentiment"].fillna(0.0)  # 결측값 처리

# 유사도 계산 함수
def calculate_similarity(df, selected_song_title):
    print(df[df['Title']=="​Bad Guy"])
    selected_song = df[df["Title"] == selected_song_title]
    if selected_song.empty:
        print("good~")
        raise ValueError(f"Selected song '{selected_song_title}' not found in the dataset.")

    

    # selected_emotions = np.array(selected_song["NRC_emotion_vector_norm"].iloc[0])
    selected_emotions = preprocess_emotion_vectors(selected_song["NRC_emotion_vector_norm"].iloc[0])
    # selected_emotions = np.array(selected_emotions)
    selected_polarity = selected_song["vader_sentiment"].iloc[0]
    selected_category = selected_song["NRC_emotion_dominant"].iloc[0]

    # Filter songs in the same category
    category_songs = df[df["NRC_emotion_dominant"] == selected_category]

    # 유클리드 거리 계산
    def euclidean_distance(row):
        emotions = preprocess_emotion_vectors(row["NRC_emotion_vector_norm"])
        emotions = np.array(emotions)
        polarity = row["vader_sentiment"]
        # emotions = np.array(emotions, dtype=float)
        # print(type(selected_emotions))
        # print(type(emotions))
        # print(type(selected_polarity))
        # print(type(polarity))
        # print(selected_emotions.dtype)  # 배열의 dtype 확인
        # print(emotions.dtype)   

        # print(emotions)
        # print(selected_polarity)
        # print(polarity)
        
        

        return np.linalg.norm(selected_emotions - emotions) + np.linalg.norm(selected_polarity - polarity)
        # return abs(selected_polarity - polarity)

    # 거리 계산 및 정렬
    category_songs = category_songs[category_songs["Title"] != selected_song_title]
    category_songs["Distance"] = category_songs.apply(euclidean_distance, axis=1)
    

    return category_songs

# 가장 가까운 노래 반환 함수
def get_closest_song(df, selected_song_title):
    result = calculate_similarity(df, selected_song_title)
    if result.empty:
        raise ValueError("No other songs in the same category.")
    return result.loc[result["Distance"].idxmin()]

# 사용 예시
selected_song_title = "NASA"
try:
    closest_song = get_closest_song(df, selected_song_title)
    print("Closest Song:")
    print(closest_song)
except ValueError as e:
    print(e)
