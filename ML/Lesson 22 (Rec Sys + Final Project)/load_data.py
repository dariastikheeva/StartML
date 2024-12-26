import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def load_raw_data():
    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml")

    def load_data(table_name, limit=None):
        query = f"SELECT * FROM public.{table_name}"
        if limit:
            query += f" LIMIT {limit}"
        with engine.connect() as connection:
            data = pd.read_sql(query, con=connection)
        return data

    user_df = load_data("user_data")
    post_df = load_data("post_text_df")
    feed_df = load_data("feed_data", limit=1000000)

    return user_df, post_df, feed_df


def create_features(user_df, post_df, feed_df):

    cols_for_ohe = ['gender', 'country', 'exp_group', 'os', 'source']
    X = user_df[cols_for_ohe]

    OHE = OneHotEncoder(drop='first')
    X_trans = OHE.fit_transform(X).toarray()

    col_names = OHE.get_feature_names_out()
    OHE_user = pd.DataFrame(X_trans, columns=col_names)

    OHE_user = OHE_user.astype(int)
    user_df = pd.concat([user_df['user_id'], user_df['age'], OHE_user], axis=1)

    len_text = post_df['text'].apply(lambda x: len(x))
    post_df['text_len'] = len_text

    def tfidf_vectorization(dataset: pd.DataFrame, to_vector: str):
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(dataset[to_vector])

        max_tfidf_values = tfidf_matrix.max(axis=1).toarray().flatten()
        avg_tfidf_values = np.ravel(tfidf_matrix.mean(axis=1).flatten())

        dataset['max_tfidf'] = max_tfidf_values

        return dataset

    tmp = tfidf_vectorization(post_df, to_vector='text')
    post_df = tmp.drop('text', axis=1).copy()

    feed_df = feed_df[feed_df['action'] == 'view']

    feed_df = feed_df.sort_values('timestamp').reset_index(drop=True)

    df = feed_df.merge(user_df, how='left').merge(post_df, how='left')

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    def parse_time(time, type_):
        if type_ == 'month':
            return time.month
        if type_ == 'day':
            return time.day
        if type_ == 'hour':
            return time.hour
        if type_ == 'minute':
            return time.minute

    def parse_date_time(data):
        data['month'] = data['timestamp'].apply(parse_time, type_='month')
        data['day'] = data['timestamp'].apply(parse_time, type_='day')
        data['hour'] = data['timestamp'].apply(parse_time, type_='hour')
        data['minute'] = data['timestamp'].apply(parse_time, type_='minute')

        data['month'] = data['month'].astype(object)
        data['day'] = data['day'].astype(object)
        data['hour'] = data['hour'].astype(object)
        data['minute'] = data['minute'].astype(object)
        return data

    df = parse_date_time(df)

    df = df.drop('timestamp', axis=1)

    return df


def load_to_sql(table_name, data):
    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml")

    data.to_sql(table_name, con=engine, if_exists='replace',
                index=False, chunksize=10000)


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000

    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml")

    conn = engine.connect().execution_options(stream_results=True)
    chunks = []

    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)

    conn.close()

    return pd.concat(chunks, ignore_index=True)


def load_features() -> pd.DataFrame:
    query = "SELECT * FROM darja_stiheeva_lms4973_features_lesson_22"

    return batch_load_sql(query)


user_df, post_df, feed_df = load_raw_data()

df = create_features(user_df, post_df, feed_df)

table_name = 'darja_stiheeva_lms4973_features_lesson_22'
load_to_sql(table_name, df)

features = load_features()
print(features.head())