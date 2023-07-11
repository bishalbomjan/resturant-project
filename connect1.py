
import json
import psycopg2
import os
import django
import datetime
# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Restaurant_Core.settings")
django.setup()
from django.contrib.auth.models import User
# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="restaurant",
    user="postgres",
    password="human#123"
)

# Open a cursor
cur = conn.cursor()
# cur.execute("ALTER SEQUENCE res_restaurant_id_seq RESTART WITH 1")
# cur.execute("ALTER SEQUENCE res_image_id_seq RESTART WITH 1")
# cur.execute("ALTER SEQUENCE res_cuisine_id_seq RESTART WITH 1")
# cur.execute("ALTER SEQUENCE res_restaurant_cuisine_id_seq RESTART WITH 1")
# cur.execute("ALTER SEQUENCE res_restaurant_rating_id_seq RESTART WITH 1")
# if conn:
#     print("Connection successful!")

# Read the JSON file
with open("C:/Users/bisha/OneDrive/Desktop/New folder/changed_data_rating.json",encoding="utf-8") as f:
    data = json.load(f)

# Loop through each restaurant in the data dictionary
for i,restaurant in enumerate(data):
    user_name='owner'+str(i)
    user = User.objects.create_user(
        username=user_name,
        first_name='Owner',
        last_name='restaurant',
        email='owner'+str(i)+'@gmail.com',
        password='Idontknow12',
        is_active=True,
        is_superuser=False,
        is_staff=False
    )
    user_id=user.id
    # Insert a new row into the restaurants table
    # slug=restaurant['name'].replace(" ","-").replace("'","").replace("&","").replace(":","").replace("+","").replace("=","").lower()
    slug = restaurant['name'].replace(" ", "-").replace("'", "").replace("&", "").replace(":", "").replace("+", "").replace("=", "").lower()
    for symbol in "!@#$%^*()_<>?,./|~`:;'\"[]{}éā´’íñ":
        slug = slug.replace(symbol, "")

    cur.execute(
        "INSERT INTO restaurant_restaurant (name, location, longitude, latitude, capacity, average_rating, number_of_reviews,slug,num_bookings) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s) RETURNING id",
        (restaurant["name"], restaurant["location"], restaurant["longitude"], restaurant["latitude"], restaurant["capacity"], restaurant["average_rating"], restaurant["number_of_reviews"],slug,0)
    )
    restaurant_id = cur.fetchone()[0]

    # Loop through each image URL and insert a new row into the images table
    for image_url in restaurant["image_url"]:
        cur.execute(
            "INSERT INTO restaurant_image (url, restaurant_id,image_name) VALUES (%s, %s,%s)",
            (image_url, restaurant_id,'ok')
        )

    # Loop through each cuisine and insert a new row into the cuisines and restaurant_cuisines tables
    for cuisine in restaurant["cuisine"]:
        cur.execute(
            "SELECT id FROM restaurant_cuisine WHERE name = %s",
            (cuisine,)
        )
        cuisine_row = cur.fetchone()
        if cuisine_row:
            cuisine_id = cuisine_row[0]
        else:
            cur.execute(
                "INSERT INTO restaurant_cuisine (name) VALUES (%s) RETURNING id",
                (cuisine,)
            )
            cuisine_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO restaurant_restaurantcuisine (restaurant_id, cuisine_id) VALUES (%s, %s)",
            (restaurant_id, cuisine_id)
        )
    for ratings in restaurant["rating"]:
        username=ratings["username"]
        u_id=ratings["u_id"]
        rating=ratings["rated"][0]
        comment=ratings["comment"]
        cur.execute(
                    "INSERT INTO restaurant_ratings (restaurant_id,username, rating, body) VALUES (%s,%s, %s, %s)",
                    (restaurant_id,username, rating, comment)
                )
    cur.execute(
        "INSERT INTO restaurant_userprofile (user_id, is_owner,new_rated) VALUES (%s,%s,%s)",
        (user_id,True,False)
    )
    cur.execute(
        "INSERT INTO user_ownerrestaurant (owner_id, restaurant_id) VALUES (%s,%s)",
        (user_id,restaurant_id)
    )
# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()

''' cur.execute(
    "CREATE INDEX idx_restaurant_name ON restaurant_restaurant (name);"
    "INSERT INTO restaurant_restaurant (name, location, longitude, latitude, capacity, average_rating, number_of_reviews,slug,num_bookings) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s) RETURNING id",
    (restaurant["name"], restaurant["location"], restaurant["longitude"], restaurant["latitude"], restaurant["capacity"], restaurant["average_rating"], restaurant["number_of_reviews"],slug,0)
)'''