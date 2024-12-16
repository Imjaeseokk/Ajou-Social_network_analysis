import pandas as pd
import numpy as np


# Define a function to calculate the similarity score
def calculate_similarity(df, selected_song_name):
    # Ensure the input data has proper structure
    df["8 Emotions Probability"] = df["8 Emotions Probability"].apply(eval)  # Convert string to list if needed

    # Get the selected song data
    selected_song = df[df["Name"] == selected_song_name]
    if selected_song.empty:
        raise ValueError(f"Selected song '{selected_song_name}' not found in the dataset.")

    selected_emotions = np.array(selected_song["8 Emotions Probability"].iloc[0])
    selected_polarity = selected_song["Positive / Negative"].iloc[0]
    selected_category = selected_song["Category"].iloc[0]

    # Filter songs in the same category
    category_songs = df[df["Category"] == selected_category]

    # Calculate distances and add to a new column
    def euclidean_distance(row):
        # Set 1: Emotion distances
        emotions = np.array(row["8 Emotions Probability"])
        set1_distance = np.linalg.norm(selected_emotions - emotions)

        # Set 2: Polarity distance
        polarity = row["Positive / Negative"]
        set2_distance = np.linalg.norm(selected_polarity - polarity)

        # Similarity Score
        similarity_score = np.sqrt((set1_distance - set2_distance) ** 2)
        return similarity_score

    category_songs["Distance"] = category_songs.apply(euclidean_distance, axis=1)
    return category_songs


# Example DataFrame (mock data for testing purposes)
data = {
    "Name": ["Song A", "Song B", "Song C", "Song D"],
    "Positive / Negative": [0.8, -0.2, 0.1, -0.5],
    "Sub": [1, 0, 1, 0],
    "8 Emotions Probability": ["[0.8,0.2,0,0,0,0,0,0]", "[0.1,0.3,0.2,0.1,0.1,0.1,0.05,0.05]",
                               "[0.7,0.1,0.1,0.05,0.05,0,0,0]", "[0.05,0.05,0.2,0.3,0.3,0.05,0.05,0.05]"],
    "Category": ["Sad", "Happy", "Sad", "Happy"]
}
df = pd.DataFrame(data)
print(df)

# Calculate similarity for a selected song
selected_song_name = "Song A"



def get_closest_song(df, selected_song_name):
    """
    Returns the row of the song with the closest distance.

    Parameters:
        category_songs (DataFrame): DataFrame containing songs in the same category with calculated distances.

    Returns:
        Series: Row of the song with the smallest distance.
    """

    # Calculate similarity for the selected song
    result = calculate_similarity(df, selected_song_name)

    # Exclude the selected song from the results
    result = result[result["Name"] != selected_song_name]

    # Find the row with the minimum distance
    closest_song = result.loc[result["Distance"].idxmin()]

    return closest_song

closest_result = get_closest_song(df,selected_song_name)

# Display the updated DataFrame with Distance column
print(closest_result)
