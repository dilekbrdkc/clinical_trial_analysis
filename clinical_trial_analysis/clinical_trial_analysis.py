import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\dilek\Desktop\clinical_trial_analysis\data\clinical_trials_cleaned.csv")


# 2. Converting date columns to datetime type
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['Completion Date'] = pd.to_datetime(df['Completion Date'], errors='coerce')

# 3. Filtering out rows where 'Start Date' is missing
df_filtered = df.dropna(subset=['Start Date']).copy()

# 4. Creating a new column for the start year
df_filtered['Start Year'] = df_filtered['Start Date'].dt.year

# 5. Counting the number of studies starting each year
start_counts = df_filtered['Start Year'].value_counts().sort_index()

plt.figure(figsize=(12,6))
plt.plot(start_counts.index, start_counts.values, marker='o')
plt.title('Number of Clinical Trials Started per Year')
plt.xlabel('Year')
plt.ylabel('Number of Studies')
plt.grid(True)
plt.show()

# 6. Calculating the duration of each study in days
df_filtered['Duration Days'] = (df_filtered['Completion Date'] - df_filtered['Start Date']).dt.days

# 7. Calculating the average duration per start year (exclude missing durations)
avg_duration_per_year = df_filtered.dropna(subset=['Duration Days']).groupby('Start Year')['Duration Days'].mean()

plt.figure(figsize=(12,6))
plt.plot(avg_duration_per_year.index, avg_duration_per_year.values, marker='o', color='orange')
plt.title('Average Duration of Clinical Trials by Start Year (days)')
plt.xlabel('Start Year')
plt.ylabel('Average Duration (days)')
plt.grid(True)
plt.show()