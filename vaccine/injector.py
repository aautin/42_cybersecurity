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

def main():
	method, url, headers = parse_args()

	try:
		print(f"[*] Sending {method} request to {url}, with headers: {headers}")
		response = requests.request(method, url, headers=headers)

		print(f"[*] Response code: {response.status_code}")
		print(f"[*] Response body:\n{response.text}")
	except:
		print("[!] An error occurred while making the request.")

if __name__ == "__main__":
	main()