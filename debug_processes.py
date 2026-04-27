from monitor import get_running_processes

processes = get_running_processes()
print(f'Total processes: {len(processes)}')

edge_processes = [p for p in processes if 'msedge' in p['name'].lower()]
excel_processes = [p for p in processes if 'excel' in p['name'].lower()]
spotify_processes = [p for p in processes if 'spotify' in p['name'].lower()]

print(f'Edge processes: {len(edge_processes)}')
print(f'Excel processes: {len(excel_processes)}')
print(f'Spotify processes: {len(spotify_processes)}')

if edge_processes:
    for p in edge_processes[:3]:
        print(f'  {p["name"]} (PID: {p["pid"]})')
        
if excel_processes:
    for p in excel_processes[:3]:
        print(f'  {p["name"]} (PID: {p["pid"]})')
        
if spotify_processes:
    for p in spotify_processes[:3]:
        print(f'  {p["name"]} (PID: {p["pid"]})')

print('\nSample process list:')
for i, p in enumerate(processes[:10]):
    print(f'{i+1}. {p["name"]} (PID: {p["pid"]})')
