pip install -r dev-requirements.txt
docker compose -f docker-compose-dev.yml down -v
docker compose -f docker-compose-dev.yml up -d
sleep 5
pytest -v
docker compose -f docker-compose-dev.yml down -v
