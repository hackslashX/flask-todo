
# Flask Todo Application

This is a simple Flask application for a Todo application, built using Marshmallow, JWT Authentication, Flask RESTful, SQL Alchemy and Alembic.
It also has support to encrypt API responses; the latter part of the Readme has general instructions on how to decrypt it.




## Deploy using Docker

The project includes Docker Compose to instantly set up Database, Application Environment, Dependencies, and serve the APIs via Gunicorn.
The `docker.env` file has a list of sample credentials which are used to setup the environment. Please adjust them as per your requirements.
Do not use those credentials in a production environment.

On Linux, export the environment variables in your current terminal session by executing the following command from project root directory:
```bash
export $(grep -v '^#' docker.env | xargs)
```
Now execute the following command to build the containers:
```bash
docker-compose build
```
To start the containers, execute the following command:
```bash
docker-compose up
```


## Deploy Manually
These instructions are for Debian based OS. If you're using any other operating system, you might have to adjust some commands for your distribution.

### Installing Python 3.8
On Ubuntu/Debian or any distribution using `apt` package manager, run the following command:
```bash
sudo apt update && sudo apt install python3.8 python3.8-pip python3.8-dev
```
If Python 3.8 is not available for your distribution, try adding the following `PPA` and retry the above command:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

### Installing and Configuring Poetry

The project uses Poetry https://python-poetry.org/ as the Python package and dependency
manager . Execute the following command to install Poetry.

```shell
python3.8 -m pip install poetry
```

By default, Poetry creates virtual environments in your home directory. To override this
default behaviour and set Poetry to create environments inside the project folder itself,
run the following command:

```shell
poetry config virtualenvs.in-project true
```

**Note**: You might need to append _"python 3.8 -m"_ before the command if the shell is
unable to find the _poetry_ command.

- Change directory to the backend/main.
- Configure poetry to use _python 3.8_ and create the initial environment.

```shell
poetry env use $(which python3.8)
```

- Install the required dependencies from _pyproject.toml_ file.

```shell
poetry install
```

- Activate the new environment

```shell
source .venv/bin/activate
```

### Setup PostgreSQL database
To ease setup, you can use use Amazon RDS to create a Free Tier PostgreSQL database for testing. Note down the `username`, `password` and `database name` 
used in the setup process.

On Ubuntu 20.04, you can follow this excellent guide https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
to quickly setup PostgreSQL and create roles, users and database.

### Setup Environment Variables
See the `sample.env` file supplied with the repository and make the required changes, such as setting up `DATABASE_HOST`, `DATABASE_PORT`, `JWT_SECRET_KEY`, etc.
If you're using a database other than PostgreSQL, make sure to change the `DATABASE_CONNECTION_URL` with the connector of your choice.
Once you're satisfied with the changes, rename the `sample.env` file to `dev.env` and run the following script to export the variables:
```bash
source ./scripts/set_env.sh
```

### Database Migrations

The project uses Alembic to perform migrations to the database, such as adding/deleting tables, columns, etc.
Alembic configurations can be found in `backend/main/alembic`. The `env.py` file contains reference to our `Base` models and
database connection URL. Migrations version history is in `backend/main/alembic/versions`.

To generate a new migration version:

```shell
poetry run alembic revision --autogenerate -m "My awesome migrations"
```

**Note:** Alembic does not automatically includes `sqlalchemy_utils` in the migration files. Check migration version files under `backend/main/alembic/versions` and manually 
add the following import

```python
import sqlalchemy_utils
```

To apply the latest migration:

```shell
poetry run alembic upgrade head
```

Alembic documentation can be found here: https://alembic.sqlalchemy.org/en/latest/index.html

### Running the project
Head over to `backend/main` folder and run the `main.py` file to start the APIs:
```shell
python main.py
```
The application by default listens on address `0.0.0.0` and port `5000`.

You can also use `gunicorn` to serve the project. Excecute the included `start.sh` script:
```shell
./run.sh
```
## Decrypting API Responses
All API Responses are encrypted using `AES-128` encryption. All endpoints except User Creation and Sign In are encrypted by default.
Check `backend/main/app/api/deps.py` to globally disable/enable encryption. 

When a user signs in, the API sends back Access/Refresh Tokens and a unique decyption key that can be used to decrypt the responses.
Note down this key, as the key is generated in a stateless manner i.e. the backend system does not store this key anywhere in the system.
An example sign in response is as follow:
```json
{
    "msg": "User logged in successfully.",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODU5MDE2OCwianRpIjoiMjNhMzRiYWYtYjY4MS00MTllLThlODItMWQ1NmNlYzIzNzExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4NTkwMTY4LCJleHAiOjE2Njg1OTM3NjgsInNhbHQiOiI4MmI3NjMyZjhjOGUxNzE2MTBkYjQyNGVmZmM5ZTRhNyJ9.q-hb8TJ5GbD9dREiP7OxcUo2zimPHVJ8MZxv64L4hsE",
        "key": "ece84361ab78b5dfed6e33244dc1fcdc",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODU5MDE2OCwianRpIjoiOTNjOTcyNjMtYzdlYy00MzJhLTg2N2ItYTA5NjgxOWVmMGIxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjEsIm5iZiI6MTY2ODU5MDE2OCwiZXhwIjoxNjcxMTgyMTY4fQ.yyhZbNMyPAAZF8B9oJzXkWBOuhKf9H6CXDQzZEbuI7s"
    }
}
```
Note down the `key` parameter's value.

Now if you call `user/get` API, the response will be encrypted by default:
```json
{
    "msg": "User retrieved successfully.",
    "data": "fuO/FGHyS7Nnf2+iix0iNIF6IDV14k5cKjpAIXbpvEulDtc33oe+uz5d+LmAlENaYSG2sORAwi/EzVW2XCmmDXSFrrVcFkDdnNoPnucW4jRQI3uVudNYoJElTzu0cGqjThlFK9M/2QTgElE81sTxCssQ3LPUI3gMb62K9ALFC8MdJsEp5eNfASM90rhc72Vnpu7tTQ4YZRm0GEbgSf4Hk5Kq0UJXyb4FRfq52HmT7ymihrMEseI6eI6KE+H/tCDrkVJg1h6yTET8EWm5OnI56P0886Qzb7sqSsV/PYkoV1FXnWJnXekoedOeUznpobV+L3SMTEnXIpJBZo7MZFIl/ll7e3gznqdEePbJGxMJJ6M0VHw="
}
```
You can use the following Python code snippet to decrypt the response. Make sure to replace the `key` with the value returned by sign in response
and `input` with the `data` returned by other APIs.
```python
import base64
from Crypto.Cipher import AES
from io import BytesIO

input = "API_DATA_HERE"
key = "YOUR_KEY_HERE"

key = key.encode("utf-8")

stream = BytesIO()
stream.write(base64.b64decode(input))
stream.seek(0)
nonce, tag, ciphertext = [ stream.read(x) for x in (16, 16, -1) ]

cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

print(data.decode("utf-8"))
```
The decrypted response for above API will be something like this:
```json
{
   "is_active":true,
   "date_created":"2022-11-15T19:49:28.003382",
   "date_updated":"2022-11-15T19:49:28.003386",
   "last_login":"2022-11-15T19:49:28.003388",
   "last_name":"Slash",
   "email":"hackslash164@gmail.com",
   "first_name":"Hack",
   "id":1
}
```


## Postman Collection

This repository also includes Postman Collection for all endpoints. Import the provided `.json` file into Postman to test APIs.