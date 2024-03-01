import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import os;


class ContentBasedModel:
    def __init__(self, df):
        self.df = df.fillna('')
        self.tf_idf_matrix = self._create_tf_idf_matrix()
    
    def _create_tf_idf_matrix(self):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.df['review'])
        return tfidf_matrix

    def recommend(self, item_id, num_recommendations):
        item_idx = self.df.index[self.df['ID'] == item_id].tolist()[0]
        item_profile = self.tf_idf_matrix[item_idx]
        cosine_similarities = cosine_similarity(item_profile, self.tf_idf_matrix).flatten()
        related_item_indices = cosine_similarities.argsort()[::-1][1:num_recommendations+1]
        recommended_items = self.df.iloc[related_item_indices]['ID'].tolist()
        return recommended_items

class CollaborativeFilteringModel:
    def __init__(self, df):
        self.df = df.fillna('')
        self.user_item_matrix = self._create_user_item_matrix()
    
    def _create_user_item_matrix(self):
        user_item_matrix = pd.pivot_table(self.df, values='total_review', index='ID', columns='location', fill_value=0)
        return csr_matrix(user_item_matrix.values)
    
    def recommend(self, user_id, num_recommendations):
        user_idx = self.df.index[self.df['ID'] == user_id].tolist()[0]
        user_profile = self.user_item_matrix[user_idx]
        cosine_similarities = cosine_similarity(user_profile, self.user_item_matrix).flatten()
        related_item_indices = cosine_similarities.argsort()[::-1][1:num_recommendations+1]
        recommended_items = self.df.iloc[related_item_indices]['ID'].tolist()
        return recommended_items

class HybridRecommendationSystem:
    def __init__(self, content_based_model, collaborative_filtering_model, weights=None):
        self.content_based_model = content_based_model
        self.collaborative_filtering_model = collaborative_filtering_model
        self.weights = weights if weights else [0.5, 0.5]  # Default weights
    
    def recommend(self, item_id, num_recommendations):
        content_based_recommendations = self.content_based_model.recommend(item_id, num_recommendations)
        collaborative_filtering_recommendations = self.collaborative_filtering_model.recommend(item_id, num_recommendations)
        final_recommendations = content_based_recommendations + collaborative_filtering_recommendations
        return final_recommendations[:num_recommendations]

# Load dataset from CSV

df = pd.read_csv('../tourdatas.csv')

# Initialize content-based and collaborative filtering models
content_based_model = ContentBasedModel(df)
collaborative_filtering_model = CollaborativeFilteringModel(df)

# Initialize hybrid recommendation system
hybrid_system = HybridRecommendationSystem(content_based_model, collaborative_filtering_model)

# Get recommendations for an item
# item_id = df['ID'].iloc[6]
# num_recommendations = 10
# recommendations = hybrid_system.recommend(item_id, num_recommendations)
# for r in recommendations:
#     search_id = r  # Change this to the ID you want to search for

# # Filter the DataFrame to get the row with the given ID
#     filtered_row = df[df['ID'] == search_id]

# # Extract the name from the filtered row
#     name = filtered_row['location'].iloc[0]  # Assuming 'location' is the column containing names

#     print("Name associated with ID", search_id, ":", name)
# print("Recommendations:", recommendations)
