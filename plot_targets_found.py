import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the data from CSV file
data = pd.read_csv('targets_found_by_step.csv')

# Set the style for the plot
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))
sns.lineplot(x='time_step', y='targets_found', data=data, errorbar='sd')

# Customize the plot
plt.title('Targets Found as a Function of Time Step')
plt.xlabel('Time Step')
plt.ylabel('Targets Found')
plt.savefig('targets_found_plot.png', dpi=300, bbox_inches='tight')
