# Restaurant Hours API

A Flask-based API for checking which restaurants are open for a given datetime. Enjoy!

## Setup Options

### Option 1: Using Docker (Recommended)

1. Install and launch Docker.
2. Build the Docker image:

   ```bash
   docker build -t restaurant-api .
   ```

3. Run the container:

   ```bash
   docker run -p 5000:5000 restaurant-api
   ```

### Option 2: Local Python Setup

1. Install Python 3+.
2. Install the required dependencies:

   ```bash
   pip install flask
   ```

3. Run the application:

   ```bash
   python app.py
   ```

The API will start on `http://localhost:5000` in both cases.

## API Usage

### Endpoint

- GET /restaurants/open

### Parameters

- `datetime` (required): The datetime to check for, in format (YYYY-MM-DDTHH:MM:SS)

### Example Request

Check which restaurants were open on my birthday this year:

```bash
curl "http://localhost:5000/restaurants/open?datetime=2025-03-23T12:00:00"
```

### Example Response

```json
{
   "datetime":"2025-03-23T12:00:00",
   "open_restaurants":[
      "The Cowfish Sushi Burger Bar",
      "Morgan St Food Hall",
      "Beasley's Chicken + Honey",
      "Crawford and Son",
      "The Cheesecake Factory",
      "Glenwood Grill",
      "Neomonde",
      "Page Road Grill",
      "Mez Mexican",
      "Saltbox",
      "El Rodeo",
      "Tazza Kitchen",
      "Mandolin",
      "Mami Nora's",
      "Gravy",
      "Char Grill",
      "Sitti",
      "Yard House",
      "Gringo a Gogo",
      "Brewery Bhavana",
      "Dashi"
   ]
}
```

### Error Responses

The API returns error messages for:

- Missing/invalid datetime parameter (400)
- Other processing errors (500)
