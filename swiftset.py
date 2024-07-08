import os
import core.pdf.pdf as pdf_handler
import corr.website_crawler as website_crawler
import sys
import argparse
import json
from urllib.parse import urlparse

cwd = os.getcwd()

def clear_screen():
    if os.name == "nt":
        try:
            os.system("cls")
        except Exception as e:
            print(f"Error clearing screen --> \n{e}")
    else:
        try:
            os.system("clear")
        except Exception as e:
            print(f"Error clearing screen --> \n{e}")

def banner():
    print("""
      ____       _ _____    ____    __ 
     / __/    __(_) _/ /_  / __/__ / /_
    _\ \| |/|/ / / _/ __/ _\ \/ -_) __/
   /___/|__,__/_/_/ \__/ /___/\__/\__/                                 
""")

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url", help = "URL / Domain you want to scan")
    parser.add_argument("--version", help = "View the version of Swift Set", action = "store_true")
    parser.add_argument("-V", "--verbose", help = "Set the verbosity of the scan [1-5] Default:2")
    parser.add_argument("--view_scans", help = "View all scans currently installed", action = "store_true")
    parser.add_argument("--view_core", help = "View all core scans currently installed", action = "store_true")
    parser.add_argument("-H", "--headers", help = "Specify headers file for all requests")
    parser.add_argument("-C", "--cookies", help = "Specify cookies file for all requests")
    parser.add_argument("--all_scans", help = "Run all available scans", action = "store_true")
    parser.add_argument("--core_scans", help = "Run all available core scans", action = "store_true")
    parser.add_argument("--specific_scans", help = "Run some specific scans (comma seperated)")
    parser.add_argument("--report_path", help = "Sets the report path to the specified directory")
    parser.add_argument("--username_crawler", help = "Searches for the provided username across several social medias and websites")
    parser.add_argument("--website_crawler", help = "Crawl a given URL, extract further URLs, and continue crawling them up to a specified depth.", action = "store_true")
    parser.add_argument("--depth", type = int, help = "Sets the depth in which the website_crawler should go")

    return parser.parse_args()


def modules_path_gen(module_name):
    core_directory = os.path.join(cwd , "core")
    return os.path.join(core_directory , f"{module_name}.py")

def nmap_pdf_text():
    base_text = """\n
    \n###NMAP SCAN
    We scanned the following domains
    """.strip()

    return base_text

def csrf_pdf_text():
    base_text = """
    \n###CSRF Scan
    We scanned the following urls for CORS header misconfiguration
    """.strip()

    return base_text

def write_content_for_pdf(writeable):
    text_file_path = os.path.join(cwd , "core" , "pdf" , "results.txt")
    f = open(text_file_path , "a")
    f.write(writeable)
    f.close()

def main():
    clear_screen()
    banner()
    version = "beta-dev"
    args = parse()

    if args.version:
        print(f"CURRENT VERSION --> {version}")

    if args.view_core:
        cwd = os.getcwd()
        core_directory = os.path.join(cwd , "core")
        for item in os.listdir(core_directory):
            full_path = os.path.join(core_directory , item)
            if os.path.isfile(full_path):
                file_name = item.split(".")[0]
                extension = item.split(".")[1]
                valid_core_modules = ["crsf" , "ssrf" , "xss" , "sqli" , "secrets" , "crawler" , "fuzz" , "idor" , "nmap" , "subdomain_search"]
                core_info_file = os.path.join(core_directory , "core_info.json")
                f = open(core_info_file , "r")
                core_info = f.read()
                f.close()
                core_info = json.loads(core_info)
                
                if extension == "py" and file_name in valid_core_modules:
                    print(f"CORE MODULE : {file_name} | {core_info[file_name]['description']}")

    if args.core_scans:
        if args.url:
            if args.report_path:
                
                pdf_handler.initialize_state()
                if "http://" in args.url or "https://" in args.url:
                    url_to_scan = args.url
                    domain_to_scan = urlparse(url_to_scan).netloc
                else:
                    url_to_scan = f"https://{args.url}"
                    domain_to_scan = args.url

                
                print(f"STARTING ALL CORE SCANS ON {args.url}")

                scans_performed = {
                        "crsf": False,
                        "ssrf": False,
                        "xss": False,
                        "sqli": False,
                        "secrets": False,
                        "crawler": False,
                        "fuzz": False,
                        "idor": False,
                        "nmap": False,
                        "subdomain_search": False
                    }

                if os.path.isfile(modules_path_gen("nmap")):
                    print("Running NMAP scan")
                    import core.nmap as nmap_scan
                    scans_performed["nmap"] = True
                    open_tcp_ports = nmap_scan.scanner(domain_to_scan)
                    pdf_text = nmap_pdf_text()
                    pdf_text = pdf_text + f"\n###Domain:{domain_to_scan}"
                    for port in open_tcp_ports:
                        print(f"FOUND OPEN TCP PORT {port}")
                        pdf_text = pdf_text + f"\nOpen TCP port {port}"
                    write_content_for_pdf(pdf_text)

                if os.path.isfile(modules_path_gen("csrf")):
                    print("Running CSRF scan")
                    import core.csrf as csrf_scan
                    csrf_output = csrf_scan.initialize_csrf([url_to_scan])
                    csrf_pdf = csrf_pdf_text()
                    issues_found = 0
                    for csrf_url in csrf_output:
                        if csrf_url[1] == "No issue":
                            pass
                        else:
                            url_scanned = csrf_url[0]
                            csrf_issues = csrf_url[1]
                            csrf_pdf = csrf_pdf + f"\nURL Scanned: {csrf_url[0]}"
                            for issue in csrf_issues:
                                csrf_pdf = csrf_pdf + f"\nIssue found: {issue}"
                                issues_found = issues_found + 1
                    
                    if issues_found > 0:
                        write_content_for_pdf(csrf_pdf)
                    else:
                        csrf_pdf = "\nWe did not find any CORS misconfiguration issues on the URLS we scanned"
                        write_content_for_pdf(csrf_pdf)

                pdf_handler.set_output_path(args.report_path)

                
            else:
                print("No directory/location provided. Please enter one with the arg --report_path")
        else:
            print("No url/domain found. Please enter one with the arg --url")

    if args.website_crawler:
            website_crawler.crawl(args.url, args.depth)
            
        
if __name__ == "__main__":
    main()
