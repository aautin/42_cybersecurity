all:
	docker-compose up -d --build

clean:
	docker-compose down --rmi all --remove-orphans --timeout 3

re: clean all
