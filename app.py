import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_gantt(schedule):
    fig, ax = plt.subplots()
    for idx, (machine, tasks) in enumerate(schedule.items()):
        current_time = 0
        for job, processing_time in enumerate(tasks):
            start = current_time
            end = start + processing_time
            ax.broken_barh([(start, processing_time)], (idx*10, 9), facecolors=f'C{job}')
            current_time = end
    ax.set_xlabel('Time')
    ax.set_yticks([idx*10 + 5 for idx in range(len(schedule))])
    ax.set_yticklabels([f'Machine {idx+1}' for idx in range(len(schedule))])
    return fig

# Streamlit app
st.title('Job Shop Scheduling Dashboard')

# User input for number of machines and jobs
num_machines = st.slider('Select Number of Machines', 1, 10, 2)
num_jobs = st.slider('Select Number of Jobs', 1, 10, 2)

# Create an empty DataFrame to collect processing times
df = pd.DataFrame(index=[f'M{m+1}' for m in range(num_machines)], 
                  columns=[f'Job {j+1}' for j in range(num_jobs)])

# Generate input fields in a grid layout
for i in range(num_machines):
    cols = st.columns(num_jobs)
    for j in range(num_jobs):
        df.iloc[i, j] = cols[j].number_input(f'M{i+1} - Job {j+1}', min_value=1, max_value=100, value=10, key=f'{i}-{j}')

# Convert DataFrame values to integers
df = df.astype(int)

# Create schedule dictionary from DataFrame
schedule = {machine: df.loc[machine].tolist() for machine in df.index}

# Plot and display the Gantt Chart
fig = plot_gantt(schedule)
st.pyplot(fig)
