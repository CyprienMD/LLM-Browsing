import pandas as pd
import configuration

# Read the CSV file
input_file = 'targets_found_by_step.csv'  # Replace with your input file name
output_file = 'targets_found_by_step_avg.csv'  # Replace with your desired output file name

# Load the CSV data into a DataFrame
df = pd.read_csv(input_file).head(10 * configuration.learning_configurations["test_episode_length"])

# Group by the 'step' column and calculate the mean score for each step
average_scores = df.groupby('time_step')['targets_found'].mean().reset_index()

# Save the result to a new CSV file
average_scores.to_csv(output_file, index=False)

print(f"Average targets found by step have been saved to {output_file}")
