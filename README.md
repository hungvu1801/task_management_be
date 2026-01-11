`docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v ${PWD}/PgDB:/var/lib/postgresql/data -v ${PWD}/init:/docker-entrypoint-initdb.d postgres:15.15`

`docker exec -it <> psql -U postgres`

`uv run -m app.init_db`

`uv run -m app.main`
