# Letterboxd-Tweeter
[![Docker Hub](https://img.shields.io/static/v1.svg?color=086dd7&labelColor=555555&logoColor=ffffff&label=&message=docker%20hub&logo=Docker)](https://hub.docker.com/repository/docker/finiteui/letterboxd-tweeter)

This is a simple self hosted project to tweet out your Letterboxd diary entries.

The project reads Letterboxd's RSS feed using [feedparser](https://github.com/kurtmckee/feedparser) to find new diary entries for a givern user, and posts them to Twitter using [twikit](https://github.com/d60/twikit).

## Example
![image](https://github.com/user-attachments/assets/8c8263f7-3352-486c-b68d-0d8fe61ede1f)

## Deployment
The project can be run locally, but was designed to be run on Docker.

The image is hosted on [Docker Hub](https://hub.docker.com/repository/docker/finiteui/letterboxd-tweeter) and can be deploted from there.
To deploy the project on docker:
- Create a new directory and download the included [docker-compose](Source/docker-compose.yml) file into it.
- In the directory, create a file name Letterboxd-Tweeter.env with the contents defined below.
- In the terminal, navigate to this directory, and run ```docker compose up -d```

If the Letterboxd-Tweeter.env file variables are correct, you should be up and running.

## ENV File
This project relies on an env file named Letterboxd-Poster.env with configuration variables to run. An example can be found [here](Source/Letterboxd-Poster.env.example).
The file needs the following:
```
LETTERBOXD_ACCOUNT = Your Letterboxd account name
TWITTER_USER = Your Twitter use name (no @)
TWITTER_EMAIL = The email address associated with your Twitter account
TWITTER_PASSWORD = Your Twitter Password
```

While including your password may seem dangerous, this project is self hosted, and open source. The password is not stored anywhere other than the .env file, and is as secure as the machine you run the project on.
