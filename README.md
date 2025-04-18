### To run this project, please install Docker CLI

---

Build the docker image

```
docker build -t diabetes-prediction .
```

Run the docker image on the port 5000

```
docker run --init -p 5000:5000 --rm diabetes-prediction
```
