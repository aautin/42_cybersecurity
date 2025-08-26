import requests
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-x", type=str, choices=["GET", "POST"], default="GET",
		help="Type of request, if not specified GET will be used.")
	parser.add_argument("--header", action="append", nargs=2, metavar=("NAME", "VALUE"),
		help="Specify a header pair (can be used several times)")
	parser.add_argument("--body", type=str, metavar="VALUE",
		help="Specify body content for POST request")
	
	args = parser.parse_args()
	if args.body and args.x.upper() != "POST":
		parser.error("--body can only be used with -X POST")
	
	body_data = args.body if args.body else ""
	return args.x.upper(), args.url, dict(args.header) if args.header else {}, body_data

def get_query_params(url : str) -> list[tuple[str, str]]:
	if '?' in url:
		query_list = url.split('?', 1)[1].split('&')
		query_list = [param for param in query_list if '=' in param]
		return [(param.split('=', 1)[0], param.split('=', 1)[1]) for param in query_list]
	return []

def main():
	method, url, headers, body_data = parse_args()
	print(f"[*] Parsed arguments: method={method}, url={url}, headers={headers}, body_data={body_data if method == 'POST' else 'N/A'}")

	try:
		print(f"[*] Sending request with the query parameters {get_query_params(url)}")
		print(requests.request(method, url, headers=headers, data=body_data if method == "POST" else None).content)
	except:
		print("[!] An error occurred while making the request.")

if __name__ == "__main__":
	main()