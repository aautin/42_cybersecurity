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



def body_params(body_string: str) -> dict[str, str]:
	if body_string:
		body_list = body_string.split('&')
		return {param.split('=', 1)[0]: param.split('=', 1)[1] if '=' in param else '' for param in body_list}
	return {}

def body_string(body_params: dict[str, str]) -> str:
	return '&'.join([f"{key}={value}" for key, value in body_params.items()])



def query_params(query_string : str) -> dict[str, str]:
	if not query_string: return {}
	query_list = query_string.split('&')
	return {param.split('=', 1)[0]: param.split('=', 1)[1] if '=' in param else '' for param in query_list}

def query_string(query_params: dict[str, str]) -> str:
	return '&'.join([f"{key}={value}" for key, value in query_params.items()])

def extract_query_string(full_url: str) -> str:
	return full_url.split('?', 1)[1] if '?' in full_url else ''



def assemble_full_url(base_url: str, query_string: str) -> str:
	return base_url + ('?' + query_string if query_string else '')

def extract_base_url(full_url: str) -> str:
	return full_url.split('?', 1)[0]
# ----------------------- #


def default_request_record(method: str, full_url: str, headers: dict, body_string: str) -> dict:
	request = requests.request(method, full_url, headers=headers, data=body_string if method == "POST" else None)
	time = request.elapsed.total_seconds()
	for _ in range(10):
		req = requests.request(method, full_url, headers=headers, data=body_string if method == "POST" else None)
		if req.elapsed.total_seconds() > time:
			time = req.elapsed.total_seconds()

	return {
		"body": body_params(body_string),
		"query": query_params(extract_query_string(full_url)),
		"response": {
			"status_code": request.status_code,
			"content": request.content.decode(),
			"time": time
		}
	}

def detection_request_records(method: str, full_url: str, headers: dict, body_string: str) -> list[dict]:
	body_params = body_params(body_string)
	query_params = query_params(extract_query_string(full_url))
	params = body_params + query_params

	detection_request_records = []
	
	# To be continued...
	# Modify one different parameter for each request with "INJECTED" value
	# Reassemble body and query strings then request and store the response as a record in detection_request_records
	return detection_request_records

def main():
	method, url, headers, body = parse_args()

	try:
		records = {
			"default": default_request_record(method, url, headers, body),
			"detections": detection_request_records(method, url, headers, body)
		}
		# To be continued...
		# Print the records body and query parameters

	except:
		print("[!] An error occurred while making the requests.")

if __name__ == "__main__":
	main()