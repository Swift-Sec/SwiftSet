import os
import threading
import requests

cwd = os.getcwd()
output_file = os.path.join(cwd, "core", "lists", "valid_subdomains.txt")

def check(url):
    real = f"https://{url}"
    try:
        r = requests.get(real, timeout=5)
        if r.status_code == 200:
            with open(output_file, 'a') as f:
                f.write(f"{url}\n")
    except requests.RequestException:
        pass

def brute_force(domain):
    file_path = os.path.join(cwd, "core", "lists", "subdomains_long.txt")

    try:
        with open(file_path, 'r') as f:
            subdomains = f.read().splitlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    urls = [f"{item}.{domain}" for item in subdomains]

    max_threads = 10
    threads = []

    for url in urls:
        while threading.active_count() > max_threads:
            pass
        thread = threading.Thread(target=check, args=[url])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

brute_force(domain="profurry.xyz")
