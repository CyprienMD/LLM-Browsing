import json
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index
from scipy.stats import wasserstein_distance
from pyemd import emd
from data.db_interface import DBInterface

datasets = ["imdb"]
distance_matrix_10 = []
for i in range(10):
    distance_matrix_10.append([])
    for j in range(10):
        distance_matrix_10[i].append(float(abs(i-j)))
distance_matrix_10 = np.array(distance_matrix_10)
distance_matrix_5 = []
for i in range(5):
    distance_matrix_5.append([])
    for j in range(5):
        distance_matrix_5[i].append(float(abs(i-j)))
distance_matrix_5 = np.array(distance_matrix_5)

for dataset in datasets:
    with DBInterface(dataset) as db_interface:

        # T1: Top comedy
        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Comedy' order by rating desc limit 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T1.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Comedy' order by rating desc limit 25;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T1_SUB.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Comedy' order by rating desc limit 75;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T1_SUP.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Comedy' order by rating desc limit 50 offset 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T1_SIM.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Crime' order by rating desc limit 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T1_DIFF.csv", index=False
        )

        # T2: Top crime
        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Crime' order by rating desc limit 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T2.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Crime' order by rating desc limit 25;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T2_SUB.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Crime' order by rating desc limit 75;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T2_SUP.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Crime' order by rating desc limit 50 offset 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T2_SIM.csv", index=False
        )

        top_items_query = "SELECT id FROM public.elements where type = 'item' and (attributes -> 'genres')::jsonb ? 'Comedy' order by rating desc limit 50;"
        top_items_data = pd.read_sql(top_items_query, db_interface.conn)
        top_items_reviews_query = f"SELECT id FROM public.elements where item_id in ({str(top_items_data.id.to_list()).replace('[', '').replace(']', '')}) ;"
        top_items_data = pd.concat([top_items_data, pd.read_sql(
            top_items_reviews_query, db_interface.conn)])
        top_items_data.to_csv(
            f"./rl/targets/{dataset}_T2_DIFF.csv", index=False
        )

        # top_reviews_query = "SELECT id FROM public.elements where type = 'review' order by rating desc limit 100;"
        # pd.read_sql(top_reviews_query, db_interface.conn).to_csv(
        #     f"./rl/targets/{dataset}_top_reviews.csv", index=False
        # )

        sentiment_query = (
            "SELECT id, item_id, sentiments FROM public.elements where type = 'review'"
        )
        sentiment_data = pd.read_sql(sentiment_query, db_interface.conn)
        sentiment_data.sentiments = sentiment_data.sentiments.apply(
            lambda x: np.array(x, dtype=np.float))
        # item_sentiments = sentiment_data[["item_id", "sentiments"]].groupby(
        #     "item_id").sentiments.apply(np.mean).reset_index().rename({"item_id": "id"}, axis=1)
        # item_sentiments["normalized"] = item_sentiments.sentiments.apply(
        #     lambda x: x / x.sum())
        # item_sentiments.drop(columns="sentiments", inplace=True)
        sentiment_data["normalized"] = sentiment_data.sentiments.apply(
            lambda x: x / x.sum())
        # sentiment_data.rename({"item_id": "id"}, axis=1, inplace=True)
        sentiment_data.drop(columns="sentiments", inplace=True)
        distance_matrix = distance_matrix_10
        ref = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0])
        # item_sentiments["skewed_up"] = item_sentiments.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        sentiment_data["skewed_up"] = sentiment_data.normalized.apply(
            lambda x: emd(x, ref, distance_matrix))

        ref = np.array([1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # item_sentiments["skewed_down"] = item_sentiments.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        sentiment_data["skewed_down"] = sentiment_data.normalized.apply(
            lambda x: emd(x, ref, distance_matrix))

        ref = np.array([0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0.5])
        # item_sentiments["polarized"] = item_sentiments.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        sentiment_data["polarized"] = sentiment_data.normalized.apply(
            lambda x: emd(x, ref, distance_matrix))

        # item_sentiments.normalized = item_sentiments.normalized.apply(
        #     lambda x: x.tolist())
        # sentiment_data.normalized = sentiment_data.normalized.apply(
        #     lambda x: x.tolist())
        # item_sentiments.sort_values("skewed_up").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_sentiment_skewed_up.csv", index=False)
        sentiment_data.sort_values("skewed_up").iloc[:1050].to_csv(
            f"./rl/targets/{dataset}_T3.csv", index=False)
        sentiment_data.sort_values("skewed_up").iloc[:525].to_csv(
            f"./rl/targets/{dataset}_T3_SUB.csv", index=False)
        sentiment_data.sort_values("skewed_up").iloc[:1575].to_csv(
            f"./rl/targets/{dataset}_T3_SUP.csv", index=False)
        sentiment_data.sort_values("skewed_up").iloc[1050:2100].to_csv(
            f"./rl/targets/{dataset}_T3_SIM.csv", index=False)
        sentiment_data.sort_values("skewed_up", ascending=False).iloc[:1050].to_csv(
            f"./rl/targets/{dataset}_T3_DIFF.csv", index=False)
        # item_sentiments.sort_values("skewed_down").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_sentiment_skewed_down.csv", index=False)
        # sentiment_data.sort_values("skewed_down").iloc[:1050].to_csv(
        #     f"./rl/targets/{dataset}_review_sentiment_skewed_down.csv", index=False)
        # item_sentiments.sort_values("polarized").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_sentiment_polarized.csv", index=False)
        # sentiment_data.sort_values("polarized").iloc[:1050].to_csv(
        #     f"./rl/targets/{dataset}_review_sentiment_polarized.csv", index=False)

        rating_query = (
            "SELECT item_id, rating FROM public.elements where type = 'review'"
        )

        # max_rate = 10 if dataset == "imdb" else 5
        # distance_matrix = distance_matrix_10 if dataset == "imdb" else distance_matrix_5
        # rating_data = pd.read_sql(rating_query, db_interface.conn)
        # rating_data.rating = rating_data.rating.astype(int)
        # item_ratings = rating_data.groupby("item_id").rating.value_counts(normalize=True, bins=range(max_rate+1)).rename("counts").reset_index(
        # ).sort_values(by='rating').groupby("item_id").counts.apply(np.array).rename("normalized").reset_index().rename({"item_id": "id"}, axis=1)
        # ref = [0.0] * max_rate
        # ref[-1] = 1.0
        # ref = np.array(ref)
        # item_ratings["skewed_up"] = item_ratings.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        # item_ratings.sort_values("skewed_up").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_ratings_skewed_up.csv", index=False)
        # ref = [0.0] * max_rate
        # ref[0] = 1.0
        # ref = np.array(ref)
        # item_ratings["skewed_down"] = item_ratings.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        # item_ratings.sort_values("skewed_down").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_ratings_skewed_down.csv", index=False)
        # ref = [0.0] * max_rate
        # ref[-1] = 0.5
        # ref[0] = 0.5
        # ref = np.array(ref)
        # item_ratings["polarized"] = item_ratings.normalized.apply(
        #     lambda x: emd(x, ref, distance_matrix))
        # item_ratings.sort_values("polarized").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_ratings_polarized.csv", index=False)

        topics_query = (
            "SELECT id, item_id, topics FROM public.elements where type = 'review'"
        )
        topics_data = pd.read_sql(topics_query, db_interface.conn)
        topics_data.topics = topics_data.topics.apply(
            lambda x: np.array(x, dtype=np.float))
        # item_topics = topics_data[["item_id", "topics"]].groupby(
        #     "item_id").topics.apply(np.mean).reset_index().rename({"item_id": "id"}, axis=1)
        ref = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0])
        topics_data["strong_topic"] = topics_data.topics.apply(
            lambda x: wasserstein_distance(x, ref))
        # item_topics["strong_topic"] = item_topics.topics.apply(
        #     lambda x: wasserstein_distance(x, ref))
        ref = np.array([0.1]*10)
        topics_data["all_topics"] = topics_data.topics.apply(
            lambda x: wasserstein_distance(x, ref))
        # item_topics["all_topics"] = item_topics.topics.apply(
        #     lambda x: wasserstein_distance(x, ref))
        topics_data.sort_values("strong_topic").iloc[:1050].to_csv(
            f"./rl/targets/{dataset}_T4.csv", index=False)
        topics_data.sort_values("strong_topic").iloc[:525].to_csv(
            f"./rl/targets/{dataset}_T4_SUB.csv", index=False)
        topics_data.sort_values("strong_topic").iloc[:1575].to_csv(
            f"./rl/targets/{dataset}_T4_SUP.csv", index=False)
        topics_data.sort_values("strong_topic").iloc[1050:2100].to_csv(
            f"./rl/targets/{dataset}_T4_SIM.csv", index=False)
        topics_data.sort_values("strong_topic", ascending=False).iloc[:1050].to_csv(
            f"./rl/targets/{dataset}_T4_DIFF.csv", index=False)
        # topics_data.sort_values("all_topics").iloc[:1050].to_csv(
        #     f"./rl/targets/{dataset}_T4.csv", index=False)
        # topics_data.sort_values("all_topics").iloc[:525].to_csv(
        #     f"./rl/targets/{dataset}_T4_SUB.csv", index=False)
        # topics_data.sort_values("all_topics").iloc[:1575].to_csv(
        #     f"./rl/targets/{dataset}_T4_SUP.csv", index=False)
        # topics_data.sort_values("all_topics").iloc[1050:2100].to_csv(
        #     f"./rl/targets/{dataset}_T4_SIM.csv", index=False)
        # topics_data.sort_values("all_topics", ascending=False).iloc[:1050].to_csv(
        #     f"./rl/targets/{dataset}_T4_DIFF.csv", index=False)
        # item_topics.sort_values("strong_topic").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_topics_one_strong.csv", index=False)
        # item_topics.sort_values("all_topics").iloc[:100].to_csv(
        #     f"./rl/targets/{dataset}_item_topics_all.csv", index=False)
        print()
