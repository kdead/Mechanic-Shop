# Mechanic Shop API

A Flask + SQLAlchemy + Marshmallow REST API built with the Application
Factory Pattern, matching the class Mechanic Shop ERD (Customers,
Service Tickets, Mechanics, and a Many-to-Many join table between
tickets and mechanics).

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   # Mac/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. In MySQL Workbench, create a database:
   ```sql
   CREATE DATABASE mechanic_shop_db;
   ```

4. In `config.py`, replace `<YOUR MYSQL PASSWORD>` (and the database
   name, if you named it something else) with your own values.

5. Run the app:
   ```
   python run.py
   ```
   This creates all the tables (`customers`, `mechanics`,
   `service_tickets`, `service_mechanics`) on first run and starts the
   dev server at `http://127.0.0.1:5000`.

## Endpoints

### Customers — `/customers`
| Method | Route | Description |
|---|---|---|
| POST | `/` | Create a customer |
| GET | `/` | Get all customers |
| GET | `/<id>` | Get one customer |
| PUT | `/<id>` | Update a customer |
| DELETE | `/<id>` | Delete a customer |

### Mechanics — `/mechanics`
| Method | Route | Description |
|---|---|---|
| POST | `/` | Create a mechanic |
| GET | `/` | Get all mechanics |
| PUT | `/<id>` | Update a mechanic |
| DELETE | `/<id>` | Delete a mechanic |

### Service Tickets — `/service-tickets`
| Method | Route | Description |
|---|---|---|
| POST | `/` | Create a service ticket |
| GET | `/` | Get all service tickets |
| PUT | `/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket |
| PUT | `/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket |

## Sample request bodies

Create a customer (`POST /customers/`):
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-123-4567"
}
```

Create a mechanic (`POST /mechanics/`):
```json
{
  "name": "Sam Torres",
  "email": "sam@example.com",
  "phone": "555-987-6543",
  "salary": 55000.0
}
```

Create a service ticket (`POST /service-tickets/`):
```json
{
  "VIN": "1HGCM82633A004352",
  "service_date": "2026-07-06",
  "service_desc": "Brake pad replacement",
  "customer_id": 1
}
```

## Testing
Test each endpoint in Postman, then export your collection
(Collections → ... → Export) and include the exported `.json` file in
this repo before submitting.
