import requests
import argparse
import re

# --------- INPUT PARSING --------- #
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



# --------- REQUESTS --------- #
def request_record(method: str, full_url: str, headers: dict, body_string: str) -> dict:
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

def detection_request_records(method: str, full_url: str, headers: dict, _body_string: str) -> list[dict]:
	_body_params = body_params(_body_string)
	_query_params = query_params(extract_query_string(full_url))
	params = list(_body_params.keys()) + list(_query_params.keys())

	detection_request_records = []

	for param in params:
		body_params_copy = _body_params.copy()
		query_params_copy = _query_params.copy()
		if param in body_params_copy:
			body_params_copy[param] = "INJECTED"
		if param in query_params_copy:
			query_params_copy[param] = "INJECTED"

		detection_request_records.append(request_record(method, assemble_full_url(extract_base_url(full_url), query_string(query_params_copy)), headers, body_string(body_params_copy)))

	return detection_request_records
# ----------------------- #


# --------- RECORD PARSING --------- #
def _normalize_html(s: str) -> str:
    s = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def _to_lines(s: str) -> list[str]:
    s = re.sub(r'>', '>\n', s)                 # break after tags
    s = re.sub(r'(?<=[.!?])\s+', '\n', s)      # break sentences
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    return lines

def only_new_content(base_html: str, other_html: str) -> str:
    base_set = set(_to_lines(_normalize_html(base_html)))
    other_lines = _to_lines(_normalize_html(other_html))
    diff_lines = [ln for ln in other_lines if ln not in base_set]
    return '\n'.join(diff_lines)
# ----------------------- #



def print_records(default_record: dict, detection_records: list[dict]):
	print("\n[+] Default Request Record:")
	print("  - Body Parameters:", default_record["body"])
	print("  - Query Parameters:", default_record["query"])
	print("  - Response Status Code:", default_record["response"]["status_code"])
	print("  - Response Time (s):", default_record["response"]["time"])
	content = default_record["response"]["content"]
	print("  - Response new content:\n\033[93m", content, "\033[0m\n")
	print("\n")

	print("[+] Detection Request Records:")
	for i, record in enumerate(detection_records):

		print(f"  Record {i}:")
		print("    - Body Parameters:", record["body"])
		print("    - Query Parameters:", record["query"])
		print("    - Response Status Code:", record["response"]["status_code"])
		print("    - Response Time (s):", record["response"]["time"])
		content = record["response"]["content"]
		print("    - Response new content:\n\033[93m", only_new_content(default_record["response"]["content"], content), "\033[0m\n")
		print("\n")


def main():
	method, url, headers, body = parse_args()

	try:
		records = {
			"default": request_record(method, url, headers, body),
			"detections": detection_request_records(method, url, headers, body)
		}
		# To be continued...
		# Print the records body and query parameters

		print_records(records["default"], records["detections"])

	except requests.RequestException as e:
		print("[!] An error occurred while making the requests:", e)

if __name__ == "__main__":
	main()