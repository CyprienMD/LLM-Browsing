from rl.deep_q import q_function
import configuration
import torch
import numpy as np

# Parameters:
target_variant = configuration.learning_configurations["target_variant"]
action_space_size = 50
agent_model_address = "model/amazon_T1_NOQUAL__MOO/best/model.pt"
observation_size = configuration.environment_configurations["nb_state_features"]

METHOD = 2 # 1 for postgres, 2 for csv file

# Q Function:
q_function = q_function(observation_size, action_space_size)
# loading pre-trained:
q_function.load_state_dict(torch.load(agent_model_address))


if METHOD == 2:
    import pandas as pd
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

    # loading dataset
    df = pd.read_csv("elements.csv")
    def parse(line):
        line = line.replace("{","[")
        line = line.replace("}","]")
        return ast.literal_eval(line)
    df['sentiments'] = df['sentiments'].apply(parse)
    df['topics'] = df['topics'].apply(parse)





def get_q_values(input_element_id, output_element_ids):

    # getting actual elements
    if METHOD == 1:
        # * METHOD 1: with postgres (ignore)
        from rl.boolean_state_features import StateEncoder
        from data.db_interface import DBInterface

        with DBInterface("amazon") as db_interface:

            # creating state_encoder
            state_encoder = StateEncoder(db_interface)

            # converting to pandas.core.series.Series
            output_elements = db_interface.get_elements(output_element_ids)
            input_element = db_interface.get_element(input_element_id)

    elif METHOD == 2:
        from rl.boolean_state_features import StateEncoder

        # * METHOD 2: with the csv
        state_encoder = StateEncoder(dataset)

        # converting to pandas.core.series.Series
        output_elements = pd.concat([df[df['id'] == id] for id in output_element_ids], ignore_index=True)
        input_element = df[df['id'] == input_element_id].iloc[0]


    # defining state
    state = state_encoder.state_feature_representation(
                input_element, output_elements, 0) # 0 is for target reached, but seems useless in code

    state_tensor = torch.from_numpy(state.astype(np.float32, copy=False))[None,:]

    # Calling q function:
    with torch.no_grad():
        res = q_function(state_tensor)
        q_values = res.q_values.numpy()[0] # shape: (action_space_size, )
    
    return q_values

def get_score_for_action(q_values, input_element_id, output_element_ids, relevance_function, quality_function, input_index):
    # returns the score associated to an action in the state defined by input_element_id and output_element_ids

    # use this function to get the index of an action:
    def mystify_action(relevance_function, quality_function, input_index):
        # This dictionary maps each relevance function to a code in the range [0, 4].
        relevance_function_inverse_dic = {
            "sim": 0, "summary_sim": 1, "sentiment_sim": 2, "tag_sim": 3, "attribute_sim": 4} #"topic_sim": 4
        # This dictionary maps each quality function to a code in the range [0, 3].
        quality_function_inverse_dic = {
            "none": 0} #, "diverse_numerical": 1, "diverse_review": 2, "coverage_review": 3}
        # all information will combined to obtain one unique ID.
        exploration_action_mystified = quality_function_inverse_dic[quality_function] * len(relevance_function_inverse_dic) + \
            relevance_function_inverse_dic[relevance_function] + \
            input_index * len(relevance_function_inverse_dic) * len(quality_function_inverse_dic)
        return exploration_action_mystified

    return q_values[mystify_action(*action)]


# Example:

if False:

    # picking random element ids
    if METHOD == 1:
        with DBInterface("amazon") as db_interface:
            output_element_ids = [db_interface.get_random_element_id() for i in range(11)]
            input_element_id = output_element_ids.pop(0)
    elif METHOD == 2:
        import random
        unique_ids = df['id'].unique()
        output_element_ids = random.sample(list(unique_ids), min(11, len(unique_ids)))
        input_element_id = output_element_ids.pop(0)

else:

    output_element_ids =  [40865, 39744, 37870, 37360, 41518, 40871, 40305, 38657, 40915, 41461]
    input_element_id = 38448


action = ("summary_sim", "none", 9) # example

q_values = get_q_values(input_element_id, output_element_ids)

print("Q Values:", q_values)
print("len(q_values):", len(q_values))

print(f"Score for action {action} in state ({input_element_id}, {output_element_ids}):", get_score_for_action(q_values, input_element_id, output_element_ids, *action))