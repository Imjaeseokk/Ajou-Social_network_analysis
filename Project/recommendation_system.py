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


# 수정된 유사도 계산 함수
def calculate_similarity(df, selected_song_title):
    """
    Calculate similarity scores for songs in the same category.
    """
    # Ensure 8 Emotions Probability is a list
    df["NRC_emotion_vector_norm"] = df["NRC_emotion_vector_norm"].apply(eval)  # Convert string to list if needed

    # Get the selected song details
    selected_song = df[df["Title"] == selected_song_title]
    if selected_song.empty:
        raise ValueError(f"Selected song '{selected_song_title}' not found in the dataset.")

    selected_emotions = np.array(selected_song["NRC_emotion_vector_norm"].iloc[0])
    selected_polarity = selected_song["vader_sentiment"].iloc[0]
    selected_category = selected_song["NRC_emotion_vector_dominant"].iloc[0]

    # Filter songs in the same category
    category_songs = df[df["NRC_emotion_vector_dominant"] == selected_category]

    # Calculate distances and add to a new column
    def euclidean_distance(row):
        # Emotion distances
        emotions = np.array(row["NRC_emotion_vector_norm"])
        set1_distance = np.linalg.norm(selected_emotions - emotions)

        # Polarity distance
        polarity = row["vader_sentiment"]
        set2_distance = np.linalg.norm(selected_polarity - polarity)

        # Similarity score
        similarity_score = np.sqrt((set1_distance - set2_distance) ** 2)
        return similarity_score

    # Exclude the selected song and calculate distance
    category_songs = category_songs[category_songs["Title"] != selected_song_title]
    category_songs.loc[:, "Distance"] = category_songs.apply(euclidean_distance, axis=1)

    return category_songs


# 가장 가까운 노래 반환 함수
def get_closest_song(df, selected_song_title):
    """
    Returns the row of the song with the closest distance.
    """
    result = calculate_similarity(df, selected_song_title)
    if result.empty:
        raise ValueError("No other songs in the same category.")
    return result.loc[result["Distance"].idxmin()]

def preprocess_emotion_vectors(vector_str):
    """
    Preprocess NRC_emotion_vector_norm strings:
    - Replace spaces with commas to correct the format.
    - Convert the corrected string to a Python list.
    """
    try:
        corrected_str = vector_str.replace(" ", ",")  # 공백을 쉼표로 대체
        return eval(corrected_str)
    except Exception as e:
        print(f"Error processing vector: {vector_str}, Error: {e}")
        return None

# 컬럼에 대한 전처리 적용
df["NRC_emotion_vector_norm"] = df["NRC_emotion_vector_norm"].apply(preprocess_emotion_vectors)


# 사용 예시
selected_song_title = "thank u, n"  # 선택한 노래 제목
try:
    closest_song = get_closest_song(df, selected_song_title)
    print("Closest Song:")
    print(closest_song)
except ValueError as e:
    print(e)
