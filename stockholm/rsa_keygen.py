import rsa

def main():
	n, d, e = rsa.rsa()
	rsa.save_key_in_file("key", n, d)
	rsa.save_key_in_file("key.pub", n, e)

if __name__ == "__main__":
	main()
