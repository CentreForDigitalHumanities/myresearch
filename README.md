[![Checks](https://github.com/CentreForDigitalHumanities/myresearch/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/CentreForDigitalHumanities/myresearch/actions/workflows/pr-checks.yml)

# MyResearch

Welcome to MyResearch!

MyResearch is a web application to facilitate various administrative tasks surrounding research
at Utrecht University. MyResearch will help researchers to determine which administrative tasks
they have to perform and allow them to fill in the respective forms. MyResearch also orchestrates
the workflow surrounding the approval of these forms. MyResearch is created by the PortalDev team of 
[Humanities IT](https://cdh.uu.nl/about/humanities-it-services/) (part of Centre for Digital Humanities)
for the Faculty of Humanities and the Faculty of Law, Economics and Governance.

MyResearch is currently in active development and is not ready for usage. When completed, it will
contain the following parts:

- A "roadmap" ("wegwijzer"), which helps the researcher to determine which administrative tasks they 
have to perform
- Forms to register a research project into the processing registry of the university and apply
for approval from the side of one of the applicable ethics committee

## Application architecture

MyResearch consists of two parts:

* A backend, written in Python and powered by the [Django](https://www.djangoproject.com) framework
for web applications
* A frontend, written in JavaScript using the [Vue.js](https://vuejs.org/) frontend framework in
combination with [Nuxt](https://nuxt.com/)

The backend and frontend communicate through GraphQL, which is facilitated in the frontend by 
[Graphene](https://graphene-python.org/) (including the `Graphene-Django` extension) and by 

The application is bilingual (English and Dutch). Translations of the backend part are managed by
Django using `gettext` (static strings) and the `django-modeltranslation` extension (strings in 
the database). Translations of the frontend part are managed by the `vue-i18n` extension.

The application is deployed on Utrecht University's servers using Docker containers, which allows
us to minimize the differences between the development and deployment environments.

## Running the application

This application can be run in one of three modes:

- **Local**: runs the application in development mode on your own machine.
- **Docker (development)**: runs interactive development servers in Docker containers.
- **Docker (production)**: runs the application in production mode.

The differences are outlined below.

| | Local | Docker dev | Docker prod |
| --- | --- | --- | --- |
| PostgreSQL database | On host machine | In container | In container |
| Frontend server | Nuxt development server | Nuxt development server in container | NGINX server serving a minimized static build |
| Backend server | TBD | TBD | TBD |
| Live-reloading on code changes | ✔ | ✔ | ❌ |
| Ports available | 3000 (frontend) | 5000 (NGINX), 3000 (frontend) | 5000 (NGINX) |
| Logging | Console | TBD | TBD |


## Running the application locally

### Prerequisites

- Node.js 22.16.0 (LTS) has been tested. Other versions may work.
- Python 3.11 has been tested. Other versions may work.
- PostgreSQL (for local database)

### Steps
1. Clone the repository and navigate to it:
   ```bash
   git clone https://github.com/CentreForDigitalHumanities/myresearch
   cd myresearch
   ```

2. Install frontend dependencies:
    ```bash
    cd frontend
    npm install
    ```

3. Start the frontend:
    ```bash
    npm run dev
    ```

4. Open your browser and navigate to `http://localhost:3000` to visit the application!

    (TODO: add backend install instructions).

5. For development, the backend requires supplementing the settings.py with a
local_settings.py file, which contains the following settings:

    ```
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

    CSRF_TRUSTED_ORIGINS = ["http://*:3000"]
    ```

6. Create a new local development database. The first PostgreSQL start-up will
normally do this for you, but in case you need to do this manually, follow this
step. The Django development server expects a database with the following
details. (This can be changed as needed in `settings.py`):
- DB name: `myresearch`
- Host: `localhost`
- Port: `5432`
- User: `myresearch`
- Password: `myresearch`

The file `backend/create_db.sql` can be used to create the database and user 
with the correct permissions. Run it as follows.

```bash
psql -U <your-postgres-username> -f backend/create_db.sql
```

Note that this is not needed if you are using the provided Docker setup. Also, 
make sure to never use these standard settings in a production environment.


## Running the application in Docker

This will start a Docker Compose network with the following containers:

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/CentreForDigitalHumanities/myresearch
   cd myresearch
   ```

2. Build the Docker images:

   ```bash
   # In development mode:
   docker compose --profile dev up --build -d

   # In production mode:
   docker compose --profile prod up --build -d
   ```

    For subsequent runs, you may omit `--build`, unless you switch branches, update dependencies or edit `compose.yml` or one of the `Dockerfile`s. This will ensure that the images are rebuilt with the latest changes.

3. Open your browser and navigate to `http://localhost:5000` to visit the application!
