## Using Compose

```
 docker compose up -d --build
```

```
docker compose ps
NAME                    IMAGE            COMMAND                  SERVICE   CREATED              STATUS              PORTS
using-compose-app-1     node:21-alpine   "docker-entrypoint.s…"   app       About a minute ago   Up About a minute   0.0.0.0:3000->3000/tcp
using-compose-mysql-1   mysql:8.0        "docker-entrypoint.s…"   mysql     About a minute ago   Up About a minute   3306/tcp, 33060/tcp
```


