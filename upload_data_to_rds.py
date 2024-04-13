import numpy as np
import pandas as pd
# import psycopg2 as ps

movies_data_path = "ml-25m/movies.csv"
links_data_path = "ml-25m/links.csv"

host_name = 'database-XXXX.us-west-1.rds.amazonaws.com'
dbname = 'XXXX'
port = '5432'
username = 'XXXX'
password = 'XXXXX'


def separateTitleYear(title):
    title = title.strip(" ")
    if title[-1] == ")" and title[-6] == "(":
        year = title[-5:-1]
        title = title[:-6]
    else:
        year = "0"

    return title + "||" + year

def process_and_transform_data(movies_data_path, links_data_path):
    movies_df = pd.read_csv(movies_data_path)
    links_df = pd.read_csv(links_data_path)

    movies_df = pd.merge(movies_df, links_df, on="movieId")
    movies_df['tmdbId'] = movies_df['tmdbId'].fillna(0)
    movies_df['tmdbId'] = movies_df['tmdbId'].astype(int)

    movies_df['title'] = movies_df['title'].apply(lambda x: separateTitleYear(x))
    movies_df['year'] = movies_df['title'].apply(lambda x: int(x.split("||")[1]))
    movies_df['title'] = movies_df['title'].apply(lambda x: x.split("||")[0])
    return movies_df

def connect_to_db(host_name, dbname, port, username, password):
    try:
        conn = ps.connect(host=host_name, database=dbname, user=username,
                          password=password, port=port)

    except ps.OperationalError as e:
        raise e
    else:
        print('Connected!')
        return conn


def create_table(curr, tablename):
    create_table_command = ("""CREATE TABLE IF NOT EXISTS %s (
                   video_id VARCHAR(255) PRIMARY KEY,
                   video_title TEXT NOT NULL,
                   upload_date DATE NOT NULL DEFAULT CURRENT_DATE,
                   view_count INTEGER NOT NULL,
                   like_count INTEGER NOT NULL,
                   dislike_count INTEGER NOT NULL,
                   comment_count INTEGER NOT NULL
           )""")

    curr.execute(create_table_command, [ps.extensions.AsIs(tablename)])


if __name__ == "__main__":
    movies_df = process_and_transform_data(movies_data_path, links_data_path)
    movies_df.to_csv("ml-25m/movies_data.csv", index=False)

    # conn = connect_to_db(host_name, dbname, port, username, password)
    # curr = conn.cursor()
    #
    # TABLE_NAME = "videos"
    # create_table(curr, TABLE_NAME)