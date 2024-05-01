import requests
from urllib.parse import urljoin

ANSI_RED = "\033[91m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"

def get_robots_txt(url):
    
    base_url = urljoin(url, "/")

    
    robots_url = urljoin(base_url, "robots.txt")
    response = requests.get(robots_url)
    if response.status_code != 200:
        print("Failed to fetch robots.txt:", response.status_code)
        return

     lines = response.text.splitlines()
    user_agent = ""
    crawl_rules = []
    for line in lines:
        if line.lower().startswith("user-agent:"):
            user_agent = line.split(":")[1].strip()
        elif line.lower().startswith(("allow:", "disallow:")):
            rule = line.split(":")[1].strip()
            crawl_rules.append((user_agent, rule))

      print(ANSI_BOLD + "Crawl Rules for", base_url + ANSI_RESET)
    for user_agent, rule in crawl_rules:
        print(ANSI_YELLOW + "User-Agent:", user_agent + ANSI_RESET)
        if "allow" in rule:
            print(ANSI_GREEN + "Allow:", rule + ANSI_RESET)
        else:
            print(ANSI_RED + "Disallow:", rule + ANSI_RESET)
        print()

# Example usage
url = input("Enter a URL: ")
get_robots_txt(url)
