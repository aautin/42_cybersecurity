all: build up

up:
	docker-compose up -d
down:
	docker-compose down

build:
	docker-compose build

restart:
	docker-compose restart

clean:
	docker-compose down --rmi all --remove-orphans --timeout 3

fclean: clean
	docker volume rm vaccine_db_data

re: clean all

fre: fclean all