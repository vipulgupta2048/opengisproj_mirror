# Yamuna River GIS Project [Private]
GIS Open Source Project.
This project uses Postgresql. Install postgresql server and pgadmin4 for easy
management of database during development phase

# Demonstration
For a brief overview of all the features included in the website, please refer to the Demo folder in the repository.   

# How to Install

### Create a virtual environemnt to start with.
```
python -m venv VENV_NAME
```

### Clone the repo.
```
git clone https://github.com/YOUR_GITHUB_FORK_URL
```

### Activate the venv
Windows:
```
VENV_NAME/Scripts/activate
```
Linux
```
source VENV_NAME/bin/activate
```
### Install the requirements
Navigate to cloned_repo/
```
pip install -r requirements.txt
```
### Create a .env file
Create a .env file in project_dir/cloned_repo/opengisproj/opengisproj with
following data:
```
DEBUG=true
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASS=your_database_pass
DATABASE_HOST=your_database_host
DATABASE_PORT=your_database_port
```

### Create the initial database tables
Navigate to cloned_repo/opengisproj/
```
python manage.py migrate
```

### Create the initial superuser
Navigate to clones_repo/opengisproj/
```
python manage.py createsuperuser
```
Fill up the required info

### Start the server
```
python manage.py runserver
```

Check the installation at http://127.0.0.1:8000/
