up:
	docker compose -f compose.dev.yaml up --build -d bot
down:
	docker compose -f compose.dev.yaml down
restart:
	docker compose -f compose.dev.yaml restart
bot:
	docker exec -it bot bash
db:
	docker exec -it database bash
