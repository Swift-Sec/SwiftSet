import os
import json
import random
import requests
from urllib.parse import urlparse
import string

cwd = os.getcwd()

def generate_random_string():
    letters = string.ascii_letters
    random_string = ""
    length = random.randint(4 , 7)
    for i in range(length):
        randomized = random.choice(letters)
        random_string = random_string + randomized
    return random_string
    

def scan_url(url , headers):

    domain = urlparse(url).netloc
    protocol = urlparse(url).scheme

    
    #checking if it needs cors
    current_issues = []
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        pass
    else:
        return [url , "No issue"]

    #wildcard scan
    headers["Origin"] = url
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        if acao_header == "*":
            current_issues.append("Wildcard allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["access-control-allow-credentials"]
            current_issues.append("Credentials allowed")
        return [url , current_issues]

    #pre domain wildcard scan
    random_letters = generate_random_string()
    headers["Origin"] = f"{protocol}://{random_letters}{domain}"
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        current_issues.append("Pre domain wildcard allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["acess-control-allow-credentials"]
            current_issues.append("Credentials allowed")
        
    #post domain wildcard scan
    random_letters = generate_random_string()
    domain_split = domain.split(".")
    domain_name = domain_split[0].strip()
    domain_tld = domain_split[1].strip()
    headers["Origin"] = f"{protocol}://{domain_name}{random_letters}.{domain_tld}"
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        current_issues.append("Post domain wildcard allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["acess-control-allow-credentials"]
            if "Credentials allowed" not in current_issues:
                current_issues.append("Credentials allowed")

    #null origin
    headers["Origin"] = "null"
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        current_issues.append("Null subdomain allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["acess-control-allow-credentials"]
            if "Credentials allowed" not in current_issues:
                current_issues.append("Credentials allowed")

    #http origin
    headers["Origin"] = f"http://{domain}"
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        current_issues.append("HTTP origin allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["acess-control-allow-credentials"]
            if "Credentials allowed" not in current_issues:
                current_issues.append("Credentials allowed")

    #checking is parser is broken
    random_letters = generate_random_string()
    tlds = [".com" , ".gov" , ".net" , ".edu" , ".org" , ".mil" , ".io" , domain_tld]
    headers["Origin"] = f"http://{domain}%60.{random_letters}.{random.choice(tlds)}"
    response = requests.get(url, headers=headers)
    response_headers = response.headers
    if "access-control-allow-origin" in response_headers.keys():
        acao_header = response_headers["access-control-allow-origin"]
        current_issues.append("HTTP origin allowed")
        if "access-control-allow-credentials" in response_headers.keys():
            acac_header = response_headers["acess-control-allow-credentials"]
            if "Credentials allowed" not in current_issues:
                current_issues.append("Credentials allowed")

    #checking code hosting platforms
    code_hosting_platforms = os.path.join(cwd, "core", "lists" , "cors_platforms.json")
    f = open(code_hosting_platforms , "r")
    code_hosting_platforms = f.read()
    f.close()

    code_hosting_platforms = json.loads(code_hosting_platforms)
    for platform in code_hosting_platforms:
        random_letters = generate_random_string()
        headers["Origin"] = f"https://{random_letters}.{platform}"
        response = requests.get(url, headers=headers)
        response_headers = response.headers
        if "access-control-allow-origin" in response_headers.keys():
            acao_header = response_headers["access-control-allow-origin"]
            current_issues.append(f"Code hosting platform {platform} allowed")
            if "access-control-allow-credentials" in response_headers.keys():
                acac_header = response_headers["acess-control-allow-credentials"]
                if "Credentials allowed" not in current_issues:
                    current_issues.append("Credentials allowed")

    if len(current_issues) ==0:
        return [url , "No issue"]
    else:
        return [url , current_issues]

def initialize_csrf(url_list , headers=False , user_agent_randomization=False):
    all_cors_issues = []
    if headers:
        pass
    else:
        headers = {
            "Accept-Language": "en-US,en;q=0.6",
            "Accept-Encoding": "gzip, deflate, br, zstd"
        }

    if user_agent_randomization:
        user_agent_file = os.path.join(cwd, "core", "lists" , "user_agents.txt")
        f = open(user_agent_file , "r")
        all_useragents = []
        for line in f:
            all_useragents.append(line.strip())
        f.close()
        user_agent = random.choice(all_useragents)

        headers["User-Agent"] = user_agent
    else:
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"

    for url in url_list:
        issues = scan_url(url.strip(), headers)
        all_cors_issues.append(issues)

    return all_cors_issues
