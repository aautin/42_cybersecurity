import requests
import argparse

# --------- PARSING --------- #
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-X", type=str, choices=["GET", "POST"], default="GET",
		help="Type of request, if not specified GET will be used.")
	parser.add_argument("--header", action="append", nargs=2, metavar=("NAME", "VALUE"),
		help="Specify a header pair (can be used several times)")
	parser.add_argument("--body", type=str, metavar="VALUE",
		help="Specify body content for POST request")
	
	args = parser.parse_args()
	if args.body and args.X.upper() != "POST":
		parser.error("--body can only be used with -X POST")
	
	body_data = args.body if args.body else ""
	return args.X.upper(), args.url, dict(args.header) if args.header else {}, body_data

def get_query_params(url : str) -> dict[str, str]:
	if '?' in url:
		query_list = url.split('?', 1)[1].split('&')
		query_list = [param for param in query_list if '=' in param]
		return {param.split('=', 1)[0]: param.split('=', 1)[1] for param in query_list}
	return {}

def get_body_params(body_data: str) -> dict[str, str]:
	if body_data:
		body_list = body_data.split('&')
		return {param.split('=', 1)[0]: param.split('=', 1)[1] for param in body_list if '=' in param}
	return {}
# ----------------------- #


def get_default_request_record(method: str, url: str, headers: dict, body: dict) -> dict:
	request = requests.request(method, url, headers=headers, data=body if method == "POST" else None)
	time = request.elapsed.total_seconds()
	for _ in range(10):
		req = requests.request(method, url, headers=headers, data=body if method == "POST" else None)
		if req.elapsed.total_seconds() > time:
			time = req.elapsed.total_seconds()

	return {
		"body": get_body_params(body) if method == "POST" else {},
		"query": get_query_params(url),
		"response": {
			"status_code": request.status_code,
			"content": request.content.decode(),
			"time": time
		}
	}

def main():
	method, url, headers, body = parse_args()

	try:
		default_record = get_default_request_record(method, url, headers, body)
		print(f"[*] Default request record: {default_record}")

	except:
		print("[!] An error occurred while making the request.")

if __name__ == "__main__":
	main()