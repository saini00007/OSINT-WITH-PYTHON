import requests
import re
from urllib.parse import urlparse

            
def check_url(url):
    try:
             if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
            
             if re.match(r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$', url):
            #return url
            pass
        else:
            raise ValueError("Invalid URL format. Please enter a valid URL.")

        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            raise ConnectionError(f"The URL '{url}' is not responding or invalid url. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"The URL '{url}' is invalid or not responding.")


def check_headers(url, headers_to_check):
	try:
		response = requests.get(url)
		response_headers = response.headers
		
		for header in headers_to_check:
			if header in response_headers:
				print("{} {:<30}: {:>10}".format("[+]", header, "YES"))
			else:
				print("{} {:<30}: {:>10}".format("[-]", header, "NO")) 

	except requests.exceptions.RequestException as e:
		print(f"Error occured durint the request: {e}")

if __name__ == "__main__":
    text = "\nHTTP Security\n"
    print(text)
    headers_to_check = ["strict-transport-security", "x-frame-options", "x-content-type-options","x-xss-protection", "content-security-policy"]
    try:
        url = input("Enter URL: ")
        valid_url = check_url(url)
        check_headers(valid_url, headers_to_check)
    except Exception as e:
        print("{} {}".format("\nError: ", e))
