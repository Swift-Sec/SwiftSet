import os
import threading
import requests
import random

cwd = os.getcwd()
output_file = os.path.join(cwd, "core", "lists", "valid_subdomains.txt")

def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"User agents file not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading user agents file: {e}")
        return []

def load_proxies(file_path):
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"Proxies file not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading proxies file: {e}")
    return proxies

def check(url, proxies, user_agents):
    real = f"https://{url}"
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    proxy = random.choice(proxies)
    proxies_dict = {
        "http": proxy,
        "https": proxy
    }

    try:
        r = requests.get(real, timeout=5, headers=headers)
        if r.status_code == 200:
            with open(output_file, 'a') as f:
                f.write(f"{url}\n")
    except requests.RequestException:
        pass

def brute_force(domain):
    file_path = os.path.join(cwd, "core", "lists", "subdomains_long.txt")
    user_agents_path = os.path.join(cwd, "core", "lists", "useragents.txt")
    proxies_path = os.path.join(cwd, "core", "lists", "proxies.txt")

    user_agents = load_user_agents(user_agents_path)
    proxies = load_proxies(proxies_path)

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
    semaphore = threading.Semaphore(max_threads)
    threads = []

    def worker(url):
        with semaphore:
            check(url, proxies, user_agents)

    for url in urls:
        thread = threading.Thread(target=worker, args=[url])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

brute_force(domain="profurry.xyz")
