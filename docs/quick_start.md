# Quick Start

## Docker

### Docker Build

After cloning the repository, run the following commands in the same directory:

```bash
cd ./rmf2_scheduler
docker build . -t rmf2_scheduler:local
```

### Docker Run

After the image is built, you can run and access the container using:

```bash
docker run -it --net=host rmf2_scheduler:local bash
```

After which you can run the modules from the packages, for example `rmf2_scheduler_server_py`.

```bash
rmf2_scheduler_server_py
```

The server should be accessible on your local device on `localhost:8000` as the command was ran with `--net=host`. You can open a browser and navigate to `http://localhost:8000/docs` to see if the swagger webpage is accessible.

## Native

The first step is to start the RMF2 Scheduler Server.

The RMF2 Scheduler provides a **Sample Python Server** for the user to try out.

> [!NOTE]
>
> The Sample Python Server requires `fastapi>=0.101.0`.
>
> You can check the version using the following command
> 
> ```bash
> pip show fastapi
> ```
>
> For **Ubuntu 22.04** users,
> the system installed FastAPI needs to be upgraded using `pip`.
>
> ```bash
> pip install -U fastapi
> ```
>
> This is **NOT NEEDED** for **Ubuntu 24.04**.

To start the API server, run the following command.

```bash
rmf2_scheduler_server_py
```

Other options include

```bash
-h, --help         show this help message and exit
--host HOST        Server Host
--port PORT        Server Port
--debug            Debug Mode

```
