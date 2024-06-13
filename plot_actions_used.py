import wandb
import numpy as np
import matplotlib.pyplot as plt

import configuration

dataset = configuration.learning_configurations["dataset"]
algorithm = configuration.learning_configurations["algorithm"]
target_variant = configuration.learning_configurations["target_variant"]
transfer_variant = configuration.learning_configurations["transfer_variant"]
reward_power = configuration.environment_configurations["reward_power"]
operator_variant = configuration.exploration_configurations["operator_variant"]
reward_variant = configuration.environment_configurations["reward_variant"]


quality_functions = [ "none" ] #, "diverse_numerical", "diverse_review", "coverage_review" ]
relevance_functions = [ "sim", "summary_sim", "sentiment_sim", "tag_sim", "topic_sim", "attribute_sim" ]


# Define the project and run ID
project_name = "cyprienm/llm&databases/"
run_id = "haorday2"

name = f"{dataset}_{target_variant}_{operator_variant}_{transfer_variant}_{reward_variant}" # ? useless ?

# Fetch the run
api = wandb.Api()
run = api.run(f"{project_name}/{run_id}")

average_actions_use = {}

for action in quality_functions + relevance_functions:
    # Retrieve the log data (example: assuming the log you want is a line plot logged as 'accuracy')
    # This assumes 'accuracy' is the key in your logs
    accuracy_data = run.history(keys=[action])

    # Extract the 'accuracy' values
    accuracy_values = accuracy_data[action].values

    # Calculate the average value
    average_accuracy = np.mean(accuracy_values)

    average_actions_use[action] = average_accuracy

    print(f"Average call of action {action}: {average_actions_use[action]}")

actions = relevance_functions
average_use =  [average_actions_use[q] for q in relevance_functions]

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(average_use, labels=actions, autopct='%1.1f%%', startangle=140)
plt.title('Average Actions Uses')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart
plt.savefig('average_action_uses.png', dpi=300, bbox_inches='tight')