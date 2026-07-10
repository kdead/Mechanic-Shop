# Mechanic Shop API

A Flask + SQLAlchemy + Marshmallow REST API built with the Application
Factory Pattern, matching the class Mechanic Shop ERD (Customers,
Service Tickets, Mechanics), plus Token Authentication, Rate Limiting,
Caching, and an Inventory resource with a Many-to-Many relationship to
Service Tickets.

## Setup

1. Create and activate a virtual environment:

   python -m venv venv

   # Mac/Linux

   source venv/bin/activate

   # Windows

   venv\Scripts\activate

2. Install dependencies:

   pip install -r requirements.txt

3. In MySQL Workbench, create a database:

   CREATE DATABASE mechanic_shop_db;

4. Create a `.env` file in the project root with:

   DB_PASSWORD=your_mysql_password
   SECRET_KEY=any-random-string-for-tokens

   (`.env` is excluded from git via `.gitignore`, so your real values
   stay private.)

5. Run the app:

   python run.py

   This creates all the tables (`customers`, `mechanics`,
   `service_tickets`, `service_mechanics`, `inventory`,
   `ticket_inventory`) on first run and starts the dev server at
   `http://127.0.0.1:5000`.

## Features

- **Token Authentication** — customers have a hashed `password`. Log in
  at `/customers/login` to get a JWT, then send it as
  `Authorization: Bearer <token>` on protected routes.
- **Rate Limiting** — `/customers/login` is capped at 5 attempts/minute
  per IP, to slow down brute-force password guessing.
- **Caching** — `GET /mechanics/` is cached for 60 seconds, since the
  mechanic list is read often but changes rarely.
- **Advanced queries** — bulk edit mechanics on a ticket, mechanics
  ranked by ticket count, paginated customer list.
- **Inventory resource** — `/inventory` blueprint, many-to-many with
  service tickets (a ticket can use many parts).

## Endpoints

### Customers — /customers

| Method | Route                | Auth? | Description                                                  |
| ------ | -------------------- | ----- | ------------------------------------------------------------ |
| POST   | /                    | -     | Create a customer (password is hashed before saving)         |
| GET    | /?page=1&per_page=10 | -     | Get customers, paginated                                     |
| GET    | /<id>                | -     | Get one customer                                             |
| PUT    | /<id>                | Yes   | Update your own customer record                              |
| DELETE | /<id>                | Yes   | Delete your own customer record                              |
| POST   | /login               | -     | Log in with email + password, returns a token (rate limited) |

### Mechanics — /mechanics

| Method | Route         | Description                                     |
| ------ | ------------- | ----------------------------------------------- |
| POST   | /             | Create a mechanic                               |
| GET    | /             | Get all mechanics (cached 60s)                  |
| PUT    | /<id>         | Update a mechanic                               |
| DELETE | /<id>         | Delete a mechanic                               |
| GET    | /most-tickets | Mechanics ranked by ticket count, busiest first |

### Service Tickets — /service-tickets

| Method | Route                                      | Auth? | Description                                                  |
| ------ | ------------------------------------------ | ----- | ------------------------------------------------------------ |
| POST   | /                                          | -     | Create a service ticket                                      |
| GET    | /                                          | -     | Get all service tickets                                      |
| PUT    | /<ticket_id>/assign-mechanic/<mechanic_id> | -     | Assign a mechanic to a ticket                                |
| PUT    | /<ticket_id>/remove-mechanic/<mechanic_id> | -     | Remove a mechanic from a ticket                              |
| PUT    | /<ticket_id>/edit                          | -     | Bulk add/remove mechanics: {"add_ids": [], "remove_ids": []} |
| GET    | /my-tickets                                | Yes   | Get the logged-in customer's own tickets                     |
| PUT    | /<ticket_id>/add-part/<inventory_id>       | -     | Add a part to a ticket                                       |

### Inventory — /inventory

| Method | Route | Description   |
| ------ | ----- | ------------- |
| POST   | /     | Create a part |
| GET    | /     | Get all parts |
| GET    | /<id> | Get one part  |
| PUT    | /<id> | Update a part |
| DELETE | /<id> | Delete a part |

## API Documentation (Swagger)

Interactive API documentation is built with `flask-swagger` and
`flask-swagger-ui`. The spec lives at `app/static/swagger.yaml` and
covers every route: path, method, tags, summary/description, request
body shape, response shape, and example payloads. Token-authenticated
routes are marked with the `bearerAuth` security scheme.

1. Run the app: `python run.py`
2. Open `http://127.0.0.1:5000/api/docs/` in your browser.
3. Use "Try it out" on any endpoint to send a live request. For
   protected routes, first hit `POST /customers/login` to get a token,
   then click the padlock icon and enter `Bearer <token>`.

## Testing

Automated tests live in `tests/`, one file per blueprint
(`test_customer.py`, `test_mechanic.py`, `test_service_ticket.py`,
`test_inventory.py`), built with Python's built-in `unittest` module.
Every route has at least one test, plus negative tests for validation
errors, 404s, and missing/invalid auth tokens.

Tests run against a throwaway SQLite database (`TestingConfig` in
`config.py`) so they never touch your real MySQL data, and rate
limiting is disabled during tests so login-related tests don't get
blocked by earlier test runs.

Run the full suite:

    python -m unittest discover tests

A Postman collection (`Mechanic Shop API.postman_collection.json`) is
also included for manual/exploratory testing.

## Sample request bodies

Create a customer (POST /customers/):

{
"name": "Jane Doe",
"email": "jane@example.com",
"phone": "555-123-4567",
"password": "supersecret123"
}

Log in (POST /customers/login):

{
"email": "jane@example.com",
"password": "supersecret123"
}

Response includes a `token` — copy it into Postman's Authorization tab
(Bearer Token) for any protected route.

Create a mechanic (POST /mechanics/):

{
"name": "Sam Torres",
"email": "sam@example.com",
"phone": "555-987-6543",
"salary": 55000.0
}

Create a service ticket (POST /service-tickets/):

{
"VIN": "1HGCM82633A004352",
"service_date": "2026-07-06",
"service_desc": "Brake pad replacement",
"customer_id": 1
}

Create a part (POST /inventory/):

{
"name": "Brake Pad Set",
"price": 45.99
}

Bulk edit ticket mechanics (PUT /service-tickets/1/edit):

{
"add_ids": [2],
"remove_ids": [1]
}

## Testing

Test each endpoint in Postman, then export your collection
(Collections → ... → Export) and include the exported .json file in
this repo before submitting.
