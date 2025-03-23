import pandas as pd
import matplotlib.pyplot as plt

gs_df = pd.read_csv('../gs.csv')
sim_df = pd.read_csv('../sim.csv')

print("Ground Speed Data:")
print(gs_df.head())

print("\nSimulation Data:")
print(sim_df.head())

plt.figure(figsize=(10, 6))

plt.plot(gs_df['timestamp'], gs_df['gs_x'], label='Ground Speed X')
plt.plot(sim_df['time'], sim_df['vx'], label='Simulation VX')

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Ground Speed X vs Simulation VX')
plt.legend()

plt.figure(figsize=(10, 6))

plt.plot(gs_df['timestamp'], gs_df['gs_y'], label='Ground Speed Y')
plt.plot(sim_df['time'], sim_df['vy'], label='Simulation VY')

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Ground Speed Y vs Simulation VY')
plt.legend()

plt.show()
