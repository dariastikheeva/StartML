import os
import pandas as pd
from typing import List
from catboost import CatBoostClassifier
from fastapi import FastAPI
from schema import PostGet, Response 
from datetime import datetime
from sqlalchemy import create_engine
import hashlib

app = FastAPI()

CONN = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"\
        "postgres.lab.karpov.courses:6432/startml"

SALT = 'my_salt'

CONTROL_MODEL_PATH = 'catboost_base_model'
TEST_MODEL_PATH = 'catboost_enhanced_model'

# CONTROL_MODEL_FEATURES_TABLE_NAME =  'daria_stikheeva_base_model_post_features'
# TEST_MODEL_FEATURES_TABLE_NAME =   'daria_stikheeva_enhanced_model_post_features'


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    
    engine = create_engine(CONN)
    conn = engine.connect().execution_options(stream_results=True)
    
    chunks = []
    
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        if path == CONTROL_MODEL_PATH:
            path = '/workdir/user_input/model_control'
        elif path == TEST_MODEL_PATH:
            path = '/workdir/user_input/model_test'
    return path


def get_exp_group(id: int) -> str:
    value_str = str(id) + SALT
    value_num = int(hashlib.md5(value_str.encode()).hexdigest(), 16)
    percent = value_num % 100
    if percent < 50:
        return "control"
    elif percent < 100:
        return "test"
    return "unknown"


def load_features() -> pd.DataFrame:
    liked_posts_query = '''
        SELECT distinct post_id, user_id
        FROM public.feed_data
        WHERE action = 'like'
        LIMIT 200000
        '''
    liked_posts = batch_load_sql(liked_posts_query)

    user_features = pd.read_sql('''
        SELECT *
        FROM public.user_data ''',
        con=CONN
    )


    posts_features_model_control = pd.read_sql(f'''
        SELECT * 
        FROM daria_stikheeva_base_model_post_features''',
        con=CONN
    )

    posts_features_model_test = pd.read_sql(f'''
        SELECT *
        FROM daria_stikheeva_enhanced_model_post_features''',
        con=CONN
    )
    return [liked_posts, user_features, posts_features_model_control, posts_features_model_test]


def load_models():
    loaded_model_control = CatBoostClassifier()
    control_model_path = get_model_path(CONTROL_MODEL_PATH)

    loaded_model_test = CatBoostClassifier()
    test_model_path = get_model_path(TEST_MODEL_PATH)

    return (
        loaded_model_control.load_model(control_model_path), 
        loaded_model_test.load_model(test_model_path)
    )


model_s = load_models()

features = load_features()


def get_recommended_feed(id: int, time: datetime, limit: int):
    user_features = features[1].loc[features[1].user_id == id]
    user_features = user_features.drop('user_id', axis=1)


    exp_group = get_exp_group(id)
    if exp_group == 'control':
        user_features = user_features.drop('exp_group', axis=1)
        posts_features = features[2].drop(
            ['index', 'text', 'topic'], axis=1
        )
        content = features[2][['post_id', 'text', 'topic' ]]
    elif exp_group == 'test':
        posts_features = features[3].drop(
            ['index', 'text', 'topic'], axis=1
        )
        content = features[3][['post_id', 'text', 'topic' ]]
    else:
        raise ValueError('unknown group')

    add_user_features = dict(zip(user_features.columns, user_features.values[0]))
    user_posts_features = posts_features.assign(**add_user_features)
    user_posts_features = user_posts_features.set_index('post_id')

    user_posts_features['hour'] = time.hour
    user_posts_features['month'] = time.month


    if exp_group == 'control':
        predicts = model_s[0].predict_proba(user_posts_features)[:, 1]
    elif exp_group == 'test':
        predicts = model_s[1].predict_proba(user_posts_features)[:, 1]

    user_posts_features['predicts'] = predicts

    liked_posts = features[0]
    liked_posts = liked_posts[liked_posts.user_id == id].post_id.values
    filtered_ = user_posts_features[~user_posts_features.index.isin(liked_posts)]

    recommended_posts = filtered_.sort_values('predicts')[-limit:].index

    return Response(**{
        'exp_group': get_exp_group(id),
        'recommendations': [
            PostGet(**{
                'id': i,
                'text': content[content.post_id == i].text.values[0],
                'topic': content[content.post_id == i].topic.values[0]
            }) for i in recommended_posts
        ]
    })
    
@app.get("/post/recommendations/", response_model=Response)
def get_recommendations(id: int, time: datetime = datetime.now(), limit: int = 5) -> Response:
    return get_recommended_feed(id, time, limit)