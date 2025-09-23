# сборка образов
# прокидка изменений: сборка образа, volume до текущего пути при изменении образа
build:
	docker build -t app_code .
run:
	docker run --name app_container -v "{PWD}:/app app_code

up:
	docker compose up

reup:
	docker compose up --build

down:
	docker compose down