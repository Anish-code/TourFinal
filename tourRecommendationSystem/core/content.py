import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from string import punctuation

class Contentbased:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.preprocess_text()
        
    # Preprocess text data
    def preprocess_text(self):
        # Convert text to lowercase
        self.data['description'] = self.data['description'].apply(lambda text: text.lower())
        # Remove punctuation
        self.data['description'] = self.data['description'].apply(lambda text: ''.join([c for c in text if c not in punctuation]))
        
    # Function to recommend based on similarity scores
    def recommend(self, city):
        # Filter data based on city
        city_data = self.data[self.data['city'] == city]
        city_data.reset_index(inplace=True)

        if city_data.empty:
            print(f"No data found for the city '{city}'")
            return city_data

        # Compute TF-IDF vectors
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(city_data['description'])

        # Calculate cosine similarity
        cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get indices of filtered data
        indices = city_data.index.tolist()

        # Initialize empty list to store recommendations
        recommendations = []
        for idx in indices:
            # Get the pairwise similarity scores of all items with that item
            sim_scores = list(enumerate(cosine_sim_matrix[idx]))
            # Sort the items based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # Get the top 5 most similar items
            sim_scores = sim_scores[1:6]
            # Get the item indices
            item_indices = [i[0] for i in sim_scores]
            # Append the top 5 most similar items to recommendations list
            recommendations.extend(item_indices)

        # Deduplicate recommendations and return at most 5 most similar items
        unique_recommendations = list(set(recommendations))
        return city_data.iloc[unique_recommendations[:min(5, len(unique_recommendations))]]


def get_recommendations(self, city):
    recommendations = self.recommend(city)
    if recommendations.empty:
        print(f"No recommendations found for the city '{city}'. Here is the DataFrame containing data for '{city}':")
        print(self.data[self.data['city'] == city])
    else:
        print(recommendations)

# # Example usage:
# city = 'Namarjung'
# content_based = Contentbased('Required_data.csv')
# content_based.get_recommendations(city)
