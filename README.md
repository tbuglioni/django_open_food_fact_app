# django_open_food_fact_app

web app: Application to obtain quality food subtituts (nutriscore), authentication is required to keep favorites

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  
[![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

### Require

- Python 3.x
- modules from requirements.txt
- postgresql

## Installation and requirements.

### Install require.

- Python 3 _[Download Python](https://www.python.org/downloads/)_

### Install app.

Link to the GitHub repository : [django_open_food_fact_app](https://github.com/tbuglioni/django_open_food_fact_app)

- Fork the project : [Fork a project](https://guides.github.com/activities/forking/)
- Create a directory for the clone.<br>
- Clone : <br><br>`user@computer:~/_path_/$ git clone <repository_url>`<br><br>
- Install [postgresql](https://www.postgresql.org/download/).
- Create a database ([Official Documentation](https://www.postgresql.org/docs/))
- Add credentials(database) in .env

### Install Python's modules.

- Install requirements in virtual env. : <br><br>`pipenv install -r requirements.txt`<br>

be careful --> mac os : psycopg2-binary / windows : psycopg2

### Add your own configuration

- create file ".env" in the root of the app
- open it with your text application
- use the ".env.example" to fill it
- save it
- close your application (to make .env credentials available)
- run this commande in the terminal :
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py run_import
  python3 manage.py runserver

## Versions

1.0

## Production link

[Heroku](https://off-app-tb.herokuapp.com)

## Authors

- **Thomas Buglioni** [link](https://github.com/tbuglioni)

## License

his project is licensed under the `MIT License` - see the file [LICENSE.md](LICENSE.md) for further information
