from rl.deep_q import q_function
import configuration
import torch

target_variant = configuration.learning_configurations["target_variant"]

action_space_size = 240

agent_model_address = "model/rural-eon-382/170000_finish/model.pt"

observation_size = 179 #configuration.environment_configurations["nb_state_features"]

q_function = q_function(observation_size, action_space_size)

# loading pre-trained: deactivated while no suitable agent is available
#-q_function.load_state_dict(torch.load(agent_model_address))

# To transform a list of ids in a state embedding:

from rl.state_features import StateEncoder
from data.db_interface import DBInterface
#-from pfrl.utils.batch_states import batch_states
import numpy as np

with DBInterface("amazon") as db_interface:

    state_encoder = StateEncoder(db_interface)

    # * picking random element ids
    output_element_ids = [db_interface.get_random_element_id() for i in range(6)]
    input_element_id = output_element_ids.pop(0)

    # converting to pandas.core.series.Series
    output_elements = db_interface.get_elements(output_element_ids)
    input_element = db_interface.get_element(input_element_id)

    # defining state
    state = state_encoder.state_feature_representation(
                input_element, output_elements, 0) # 0 is for target reached, but seems useless in code

    state_tensor = torch.from_numpy(state.astype(np.float32, copy=False))[None,:]
    
    # Testing q function:

    with torch.no_grad():

        res = q_function(state_tensor)

        q_values = res.q_values.numpy()[0] # shape: (action_space_size, )