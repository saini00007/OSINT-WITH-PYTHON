import requests

def check_url(url):
    try:
        
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
            return url

    except requests.exceptions.RequestException as e:
        raise Exception(f"The URL '{url}' is invalid or not responding.") #Error: {str(e)}")
    
def get_cookie_info(url):
    response = requests.get(url)
    cookies = response.cookies
    
    cookie_info = {}
    for cookie in cookies:
        cookie_info[cookie.name] = {
            "Domain": cookie.domain,
            "Path": cookie.path,
            "Expires": cookie.expires,
            "Secure": cookie.secure
        }
    return cookie_info

if __name__ == "__main__":
    url = input("Enter URL: ")
    urla = check_url(url)
    info = get_cookie_info(urla)
    for cookie_name, cookie_data in info.items():
        print(f"Cookie: {cookie_name}")
        for key, value in cookie_data.items():
            print(f"{key}: {value}")
        print()
