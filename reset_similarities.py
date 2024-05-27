import random
import pandas as pd
from data.db_interface import DBInterface
from data.generate_review_metadata import Sentiment, Topic, Tag, LLMSimilarity, GloVESimilarity
from tqdm import tqdm
import json

MIN_REVIEW_PER_ITEM = 10
REVIEW_SAMPLE_PER_ITEM = 5
SAMPLE_SIZE = 5
CATEGORY = "laptops"
PROCESS_COUNT = 3
with DBInterface("amazon") as db_interface:
    
    elements = pd.read_sql(
            f""" select * from elements """, db_interface.conn)
    
    element_texts = [(e.id, e.text) for (i,e) in elements.iterrows()]
    
    db_interface.cur.execute( "DELETE FROM similarities;")
    
    #Sentiment(element_texts, db_interface).generate_sentiments()
    #Topic(element_texts, db_interface).generate_topics()
    #Tag(element_texts, db_interface).generate_tags()

    LLMSimilarity('voyage',
                db_interface, process_count=PROCESS_COUNT).generate_summary_review_relevance()


    # GloVESimilarity('data/glove.6B.50d.txt',
    #            db_interface, process_count=PROCESS_COUNT).generate_summary_review_relevance()
