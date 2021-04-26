# Movie API

## Installation

Install pip first
```bash
sudo apt-get install python3-pip
```
Create virtualenv (Python3.8)
```bash
$ python3.8 -m venv myvenv
```
Activate virtualenv using
```bash
source myvenv/bin/activate
```
Clone this repo
```bash
git clone https://github.com/b4isty/movie-api.git
```

### To run this project using docker
- Go to project directory 
```shell
docker-compose up --build
```

### To run the test cases go to docker web service shell by typing 
```bash
docker exec -it movie_web bash
```

And Run 
```bash
python manage.py test
```
