# сборка образов
# прокидка изменений: сборка образа, volume до текущего пути при изменении образа
build:
	docker build -t app_code .
run:
	docker run --name app_container -v "app_volume:/app app_code

up:
	docker compose up

down:
	docker compose down