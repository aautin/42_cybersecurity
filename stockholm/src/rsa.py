import subprocess
import tempfile
import os
import re
import base64

#----------------- RSA KEY GENERATION -----------------
def extract_key_component(text, label):
	pattern = rf"{label}:\n((?:\s+[0-9a-f:]+\n)+)"
	match = re.search(pattern, text, re.IGNORECASE)
	if not match:
		raise ValueError(f"Label '{label}' not found in the text")
	hex_block = match.group(1).replace(":", "").replace(" ", "").replace("\n", "")
	return int(hex_block, 16)

def rsa():
	with tempfile.TemporaryDirectory() as tmpdir:
		private_key_path = os.path.join(tmpdir, "private.pem")
		public_key_path = os.path.join(tmpdir, "public.pem")

		subprocess.run([
			"openssl", "genpkey", "-algorithm", "RSA",
			"-out", private_key_path,
			"-pkeyopt", "rsa_keygen_bits:2048"
		], check=True)

		subprocess.run([
			"openssl", "rsa", "-in", private_key_path,
			"-pubout", "-out", public_key_path
		], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		result = subprocess.run([
			"openssl", "rsa", "-in", private_key_path, "-text", "-noout"
		], capture_output=True, text=True, check=True)

		output = result.stdout

		n = extract_key_component(output, "modulus")
		d = extract_key_component(output, "privateExponent")
		e = int(re.search(r"publicExponent: (\d+)", output).group(1))

		return n, d, e
# ----------------------------------



# ----------------- RSA SAVE AND LOAD -----------------
def save_key_in_file(file_path, n, x):
	with open(file_path, "w") as f:
		n_bytesize = (n.bit_length() + 7) // 8;
		x_bytesize = (x.bit_length() + 7) // 8;
		n_b64 = base64.b64encode(n.to_bytes(n_bytesize, byteorder="big")).decode("ascii")
		x_b64 = base64.b64encode(x.to_bytes(x_bytesize, byteorder="big")).decode("ascii")
		f.write(f"RSA_KEY\n{n_b64}:{x_b64}\n")

def load_key_from_file(file_path):
	with open(file_path, "r") as f:
		header = f.readline()
		if header.strip() != "RSA_KEY":
			raise ValueError("Invalid key file")
		line = f.readline()

	n_b64, x_b64 = line.strip().split(':')
	n = int.from_bytes(base64.b64decode(n_b64), byteorder="big")
	x = int.from_bytes(base64.b64decode(x_b64), byteorder="big")
	return n, x

def save_key_in_string(n, x):
	n_bytesize = (n.bit_length() + 7) // 8
	x_bytesize = (x.bit_length() + 7) // 8
	n_b64 = base64.b64encode(n.to_bytes(n_bytesize, byteorder="big")).decode("ascii")
	x_b64 = base64.b64encode(x.to_bytes(x_bytesize, byteorder="big")).decode("ascii")
	return str(n_b64) + ':' + str(x_b64)

def load_key_from_string(string):
	n_b64, x_b64 = string.strip().split(':')
	n = int.from_bytes(base64.b64decode(n_b64), byteorder="big")
	x = int.from_bytes(base64.b64decode(x_b64), byteorder="big")
	return n, x
# ----------------------------------



# ----------------- USE OF RSA KEY -----------------
def rsa_encrypt(message_bytes: bytes, n: int, e: int) -> bytes:
	m_int = int.from_bytes(message_bytes, byteorder="big")
	
	if m_int >= n:
		raise ValueError("Message too large for the key size")

	c_int = pow(m_int, e, n)

	cipher_len = (n.bit_length() + 7) // 8
	return c_int.to_bytes(cipher_len, byteorder="big")

def rsa_decrypt(cipher_bytes: bytes, n: int, d: int) -> bytes:
	c_int = int.from_bytes(cipher_bytes, byteorder="big")

	m_int = pow(c_int, d, n)

	msg_len = (m_int.bit_length() + 7) // 8
	return m_int.to_bytes(msg_len, byteorder="big")
# ----------------------------------
