import requests
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	# parser.add_argument("-o", type=str, default="log.txt",
	# 	help="Archive file, if not specified it will be stored in a default one.")
	parser.add_argument("-x", type=str, choices=["GET", "POST"], default="GET",
		help="Type of request, if not specified GET will be used.")
	parser.add_argument("--header", action="append", nargs=2, metavar=("NAME", "VALUE"),
		help="Specify custom headers as pairs: -h Header-Name Header-Value. Can be used multiple times.")
	args = parser.parse_args()

	return args.x.upper(), args.url, dict(args.header) if args.header else {}

def parse_headers(headers: dict) -> list[dict]:
    result = []
    for key, value in headers.items():
        pairs = []
        for item in value.split(';'):
            item = item.strip()
            if '=' in item:
                k, v = item.split('=', 1)
                pairs.append({k: v})
        result.append({key: pairs})
    return result

def get_query_params(url : str) -> list[str]:
	if '?' in url:
		query_list = url.split('?', 1)[1].split('&')
		query_list = [param for param in query_list if '=' in param]
		return [param.split('=', 1)[0] for param in query_list]
	return []

def inject_payload(url: str, method: str = "GET", headers: dict = {}, payload: str = "' OR '1'='1") -> requests.Response:
	query_params = get_query_params(url)
	if not query_params:
		print("[!] No query parameters found in the URL.")
		return None

	response = requests.request(method, url.split('?', 1)[0], headers=headers)

	return response

def main():
	method, url, headers = parse_args()

	try:
		print(f"[*] Sending {method} request to {url}, with headers {headers} and queryies {get_query_params(url)}")
		inject_payload(url, method, headers)
	except:
		print("[!] An error occurred while making the request.")

if __name__ == "__main__":
	main()