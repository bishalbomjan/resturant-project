import pandas as pd
import heapq
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time

class KNN_RECOMMENDATION:
    def __init__(self,k) -> None:
        if k==1:
            self.k=1
        else:
            self.k=10
            self.user_item_matrix=pd.read_csv('C:/Users/Nirajan/Desktop/python 30 days/user_item_matrix.csv')
            self.user_item_matrix=self.user_item_matrix.set_index("user_id")
            self.transposed_user_item_matrix=self.user_item_matrix.T
    
    def cosine_similarity_func(self,v1,v2):
        dot_product = np.dot(v1, v2)    
        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)
        if mag1 == 0 or mag2 == 0:
            return 0
        else:
            cosine_sim = dot_product / (mag1 * mag2)
            return cosine_sim
    
    def cosine_similarity_matrix(self,selected):
        cosine_sim_df=pd.DataFrame(index=self.user_item_matrix.columns,columns=['similarities'])
        
        for col in self.user_item_matrix:
            if col== selected:
                cosine_sim_df.loc[col]=1.0
            else:
                non_zero_ratings = self.user_item_matrix[[selected, col]].dropna()
                v1 = non_zero_ratings[selected].values
                v2 = non_zero_ratings[col].values
                cosine_sim = self.cosine_similarity_func(v1, v2)
                cosine_sim_df.loc[col] = cosine_sim
        return cosine_sim_df
    
    def recommend_restaurants_user_ratings(self,selected):
        cosine_sim_df=self.cosine_similarity_matrix(selected)        
        cosine_sim=cosine_sim_df['similarities']
        sorted_restaurants=cosine_sim.sort_values(ascending=False)
        print(sorted_restaurants)
        return sorted_restaurants[1:self.k+1]
    
    def haversine(self,lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        distance=round(distance,2)
        return distance
    
# start=time.time()
# Recommendation=KNN_RECOMMENDATION(k=10)
# selected_item = 'DSquare Cafe & Restaurant'
# restaurants=Recommendation.recommend_restaurants_user_ratings(selected_item)

# print('\nRestaurants Based on User Ratings\n',restaurants,'\n')



# end=time.time()

# print(end-start)