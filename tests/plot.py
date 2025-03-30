import pandas as pd
import matplotlib.pyplot as plt

test_name = 'Case 6'
output = '6.png'
data = pd.read_csv('./results/6a.csv')
data_noise = pd.read_csv('./results/6b.csv')
start_time = 5

print("CSV Headers:")
print(data.head())

data = data[data['time'] >= start_time]
data_noise = data_noise[data_noise['time'] >= start_time]

end_time = min(data['time'].max(), data_noise['time'].max())
data = data[data['time'] <= end_time]
data_noise = data_noise[data_noise['time'] <= end_time]

def rmse(d):
    gs = d[[f'gs_{axis}' for axis in ['x', 'y', 'z']]].values
    true_gs = d[[f'true_gs_{axis}' for axis in ['x', 'y', 'z']]].values
    return ((gs - true_gs) ** 2).mean() ** 0.5

for axis in ['x', 'y', 'z']:
    plt.figure(figsize=(10, 6))

    plt.plot(data['time'], data[f'gs_{axis}'], label='ideal')
    plt.plot(data_noise['time'], data_noise[f'gs_{axis}'], label='noise')
    plt.plot(data['time'], data[f'true_gs_{axis}'], label='ground-truth', linestyle='--')

    plt.xlabel('Time [s]')
    plt.ylabel('Groundspeed [m/s]')
    plt.title(f'{test_name}: GS{axis}')
    plt.legend()

    plt.savefig(axis + '_' + output)


print(f"RMSE ideal: {rmse(data)}")
print(f"RMSE noise: {rmse(data_noise)}")

plt.show()

