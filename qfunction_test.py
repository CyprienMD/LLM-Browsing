from rl.deep_q import q_function
import configuration
import torch
import numpy as np

target_variant = configuration.learning_configurations["target_variant"]

action_space_size = 240

agent_model_address = "model/rural-eon-382/170000_finish/model.pt"

observation_size = 179 #configuration.environment_configurations["nb_state_features"]

q_function = q_function(observation_size, action_space_size)

# loading pre-trained: deactivated while no suitable agent is available
#-q_function.load_state_dict(torch.load(agent_model_address))



# * To transform a list of ids in a state embedding:


METHOD = 2

if METHOD==1:
    # * METHOD 1: avec postgres

    from rl.state_features import StateEncoder
    from data.db_interface import DBInterface

    with DBInterface("amazon") as db_interface:

        # creating state_encoder
        state_encoder = StateEncoder(db_interface)

        # picking random element ids
        output_element_ids = [db_interface.get_random_element_id() for i in range(6)]
        input_element_id = output_element_ids.pop(0)

        # converting to pandas.core.series.Series
        output_elements = db_interface.get_elements(output_element_ids)
        input_element = db_interface.get_element(input_element_id)

elif METHOD==2:
    # * METHOD 1: avec le csv

    import pandas as pd
    import random
    from rl.state_features import StateEncoder
    import ast

    # creating state_encoder
    class DummyDataset():
        def __init__(self):
            self.dataset = "amazon"        
        def get_max_text_size(self):
            return  22392 # ! TODO : calculate better
        def get_max_tag_count(self):
            return 490 # ! TODO : calculate better
    dataset = DummyDataset()

    state_encoder = StateEncoder(dataset)

    # loading dataset
    df = pd.read_csv("elements.csv")
    def parse(line):
        line = line.replace("{","[")
        line = line.replace("}","]")
        return ast.literal_eval(line)
    df['sentiments'] = df['sentiments'].apply(parse)
    df['topics'] = df['topics'].apply(parse)

    # picking random element ids
    unique_ids = df['id'].unique()
    random_ids = random.sample(list(unique_ids), min(6, len(unique_ids)))

    # converting to pandas.core.series.Series
    output_elements = pd.concat([df[df['id'] == id] for id in random_ids], ignore_index=True)    
    input_element = output_elements.iloc[0]
    output_elements.drop(index=0, inplace=True)


    


# defining state
state = state_encoder.state_feature_representation(
            input_element, output_elements, 0) # 0 is for target reached, but seems useless in code

state_tensor = torch.from_numpy(state.astype(np.float32, copy=False))[None,:]

# Testing q function:

with torch.no_grad():

    res = q_function(state_tensor)

    q_values = res.q_values.numpy()[0] # shape: (action_space_size, )

    print("q_values:", q_values)