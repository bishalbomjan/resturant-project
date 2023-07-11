# import heapq
# from math import radians, sin, cos, sqrt, atan2

# class KNN:
#     def __init__(self, *args):
#         if len(args) > 0:
#             self.k = args[0]
#         else:
#             self.k = 3 
        
#     def euclidean_distance(self,x, y):
#         return ((x['reviews'] - y['reviews']) ** 2
#                 + (x['average_rating'] - y['average_rating']) ** 2) ** 0.5

#     def find_k_nearest_neighbors(self,restaurants, target_restaurant,method):
#         if method=='normal':
#             distances = [(self.euclidean_distance(r, target_restaurant), r) for r in restaurants]
#             print('\nNormal Inside K nearest method')
#         elif method == 'nearest':
#              distances = [(self.haversine(target_restaurant['latitude'], target_restaurant['longitude'], r['latitude'], r['longitude']), r) for r in restaurants]
#              print('\nNearest Inside K nearest method')
#         else:
#             print('Send Proper Method')
#         distances.sort(key=lambda x: x[0])
#         print(distances)
#         neighbors = [r for d, r in distances[:self.k]]
#         print('\nfind_k_nearest',neighbors,'\n')
#         return neighbors

#     def recommend_restaurants(self,restaurants, user_prefs,method):
#         if method == 'normal':
#             target_restaurant = {'reviews': user_prefs['reviews'], 'average_rating': user_prefs['average_rating'],
#                           'cuisine': user_prefs['cuisine']}
#             neighbors = self.find_k_nearest_neighbors(restaurants, target_restaurant, 'normal')
#             return neighbors
#         elif method == 'nearest':
#             target_restaurant = {'latitude':user_prefs['latitude'],'longitude':user_prefs['longitude']}
#             neighbors = self.find_k_nearest_neighbors(restaurants, target_restaurant, 'nearest')
#             return sorted(neighbors, key=lambda r: r['average_rating'], reverse=True)
        
        
#     def haversine(self,lat1, lon1, lat2, lon2):
#         R = 6371
#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1
#         a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = R * c
#         print('Distance',distance)
#         return distance

import json
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
class Recommend:
    def __init__(self,*args,username):
        self.k=2
        self.user=username
        with open('C:/Users/Nirajan/Desktop/python 30 days/final data for restaurant/user_item_matrix_test.json', 'r',encoding='utf-8') as f:
            self.reviews = json.load(f)
        with open('C:/TEST FINAL YEAR/user_ratings.json', 'r',encoding='utf-8') as f:
            self.user_ratings=json.load(f)
        self.users = list(self.reviews.keys())
        self.restaurants = sorted(set.union(*[set(r.keys()) for r in self.reviews.values()]))
        self.user_ratings_sparse = csr_matrix(self.user_ratings)
        self.cosine_similarities = cosine_similarity(self.user_ratings_sparse)

    def dot(a, b,self):
        return sum([a[i] * b[i] for i in range(len(a))])

    def norm(a,self):
        return (self.dot(a, a)) ** 0.5

    def knn(self,user,k):
        user_index = self.users.index(self.user)
        similarities = self.cosine_similarities[user_index]
        indices = sorted(range(len(similarities)), key=lambda x: similarities[x], reverse=True)[:self.k]
        return [(self.users[i], similarities[i]) for i in indices]
    def recomd(self):
        recommendations = []
        for restaurant in self.restaurants:
            if restaurant in self.reviews[self.user]:
                restaurant_ratings = [0 for _ in range(self.k)]
                for i, u in enumerate(self.users):
                    if restaurant in self.reviews[u]:
                        if u in [user for user, _ in self.knn(self.user, self.k)]:
                            similarity_index = [user for user, _ in self.knn(self.user, self.k)].index(u)
                            print(similarity_index)
                            restaurant_ratings[similarity_index] = self.reviews[u][restaurant]
                            print(restaurant_ratings)
                            
                similarities = [similarity for _, similarity in self.knn(self.user, self.k)]
                print(similarities)
                
                recommendation = (restaurant, self.dot(similarities, restaurant_ratings) / sum(similarities))
            
                recommendations.append(recommendation)
                

        recommendations.sort(key=lambda x: x[1], reverse=True)
        for i, (restaurant, rating) in enumerate(recommendations[:10]):
            print('Recommendation {}: {} (predicted rating: {:.2f})'.format(i+1, restaurant, rating))
        return recommendations

