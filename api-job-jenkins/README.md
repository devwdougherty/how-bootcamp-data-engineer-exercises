## Python Requirements

pip freeze > requirements.txt

## Docker

### Building the Dockerfile
Forcing the 'yes' ```-y``` response when the linux terminal inside docker image ask about continue the installs.

```dockerfile
RUN apt-get install -y python-pip
```

### Build & Running

```bash
$ docker build -t pyjenkins . 
```

```bash
$ docker exect -it 95dd902fc7df bash -l  
```


## Jenkins

- `50000` is the encryption port of jenkins

Running on: ```localhost:8000```

- Job: exchange created with the following build steps (shell):

```bash
cd /exchange
python3 main.py
```

- Run periodically option enabled with chron job (every 3 minutes):
```bash
H/3 * * * *
```

**Note:** Chron job is not working/running
