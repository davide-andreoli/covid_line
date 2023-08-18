print("hello world")

"""
import requests
from bs4 import BeautifulSoup
from yarl import URL

superset_url = URL('https://superset.example.org/')

session = requests.Session()

# get CSRF token
response = session.get(superset_url / "login/")
soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"id": "csrf_token"})["value"]

# get cookies
session.post(
    superset_url / "login/",
    data=dict(username=username, password=password, csrf_token=csrf_token),
)

# create database
database = {
    "database_name": "my db",
    "sqlalchemy_uri": "gsheets://",
    ...
}
session.post(
    superset_url / "api/v1/database/",
    json=database,
    headers={"X-CSRFToken": csrf_token},
)

"""