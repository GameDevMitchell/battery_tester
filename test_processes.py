import psutil

def test_processes():
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                print(f"Process: {proc.info}")
                if proc.info['status'] in ['running', 'sleeping']:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error: {e}")
        
    processes.sort(key=lambda x: x['name'].lower())
    print(f'\nFound {len(processes)} processes:')
    for p in processes[:20]:
        print(f"{p['name']} (PID: {p['pid']})")

if __name__ == "__main__":
    test_processes()
