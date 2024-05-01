import ssl
import requests
import socket
from OpenSSL import crypto
from datetime import datetime
def check_url(url):
    try:
           if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
             return url

    except requests.exceptions.RequestException as e:
        raise Exception(f"The URL '{url}' is invalid or not responding.") #Error: {str(e)}")
 

def get_ssl_certificate_info(url):
    
    hostname = url.split('://')[1].split('/')[0]
    
      context = ssl.create_default_context()
    
    try:
            with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()
                if certificate is None:
                    print("Failed to retrieve SSL certificate.")
                    return
                
                      x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(ssock.getpeercert(True)))
                
                    print(f"Server's certificate: {x509.get_subject().CN}")
                
                print("SSL Certificate")
                print(f"Subject: {x509.get_subject().CN}")
                print(f"Issuer: {x509.get_issuer().CN}")
                print(f"ASN1 Curve: {x509.get_pubkey().type()}")
                print(f"NIST Curve: {x509.get_pubkey().bits()}")
                
                expires_date = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
                renewed_date = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
                
                print(f"Expires: {expires_date.strftime('%d %B %Y')}")
                print(f"Renewed: {renewed_date.strftime('%d %B %Y')}")
                
                print(f"Serial Num: {x509.get_serial_number()}")
                print(f"Fingerprint: {x509.digest('sha256').decode('utf-8')}")
                
                
    except Exception as e:
        print(f"An error occurred: {e}")
raw_input = input("enter url :")
url = check_url(raw_input)
get_ssl_certificate_info(url)
