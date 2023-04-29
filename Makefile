create-network:
	docker network create user-order-network

remove-network:
	docker network rm user-order-network

user-up:
	docker-compose -f user/docker-compose.yml up --build

user-down:
	docker-compose -f user/docker-compose.yml down --remove-orphans

order-up:
	docker-compose -f order/docker-compose.yml up --build

order-down:
	docker-compose -f order/docker-compose.yml down --remove-orphans
