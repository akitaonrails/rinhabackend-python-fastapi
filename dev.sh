export DB_URL="postgresql://user:pass@localhost:5432/rinha"
export CACHE_URL="redis://localhost:6379" 
docker compose down -v
docker compose -f docker-compose-dev.yml up -d
uvicorn app.main:app --loop uvloop --host localhost --port 9999 --reload 