# A REST API example for a blog project

## Usage
### Dev Environment
1) Run `cp .env.example .env`
2) Fill in all variables in the `.env` file if needed
3) Run `docker compose -f compose-dev.yml up`
4) Run `docker exec -it blog_api_dev uv run alembic upgrade head` to apply all migrations
5) Go to `http://localhost:8001/docs`

### Prod Environment
1) Run `cp .env.example .env`
2) Fill in all variables in the `.env` file with production ones
3) Run `docker compose -f compose.yml up -d`
4) Run `docker exec -it blog_api_dev uv run alembic upgrade head` to apply all migrations
5) Go to `http://localhost:8001/docs`
