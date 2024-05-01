import requests

def get_http_headers(url):
       if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        response = requests.head(url, allow_redirects=True)
        response.raise_for_status()
        return response.headers
    except requests.RequestException as e:
        print(f"Error accessing the webpage: {e}")
        return None

def identify_web_technologies(http_headers):
    if not http_headers:
        return None

    technologies = {
        'Server': http_headers.get('Server', 'Unknown'),
        'X-Powered-By': http_headers.get('X-Powered-By', 'Not specified'),
        'X-AspNet-Version': http_headers.get('X-AspNet-Version', 'Not specified'),
    }

    return technologies

if __name__ == "__main__":
    url = input("Enter Url :")  
    http_headers = get_http_headers(url)
    if http_headers:
        web_technologies = identify_web_technologies(http_headers)
        print("\nWeb Technologies:")
        for key, value in web_technologies.items():
            print(f"{key}: {value}")
    else:
        print("Unable to retrieve HTTP headers.")
