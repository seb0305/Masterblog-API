# Masterblog-API
A simple, production-ready RESTful API for managing blog posts in Python using Flask. Features include post creation, deletion, updating, searching, and sorting, all with clear error handling and interactive documentation via Swagger UI.

## Features
- List all blog posts with optional sorting by title or content

- Create (add) new posts with unique IDs

- Update existing posts by ID (partial update supported)

- Delete posts by ID

- Search posts by title or content using query parameters

- Interactive API documentation with Swagger UI

## Project Structure
Masterblog-API/

├── backend/
│   └── backend_app.py      # Flask API backend
├── frontend/
│   ├── static/
│   │   ├── main.js
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
│   └── frontend_app.py
├── static/
│   └── masterblog.json     # Swagger API definition file
## Installation
1. Clone the repository:
git clone https://github.com/seb0305/Masterblog-API.git
cd Masterblog-API
2. Install required Python packages:
pip install flask flask_cors flask_swagger_ui
## Usage
1. Start the Flask backend:
cd Masterblog-API
python backend/backend_app.py
By default, the API is available at http://127.0.0.1:5002/

2. View API documentation:
Open http://127.0.0.1:5002/api/docs in your browser to use Swagger UI and try out the endpoints interactively!

## API Endpoints
GET	    /api/posts	List all posts, with optional sorting
POST	/api/posts	Add a new post
PUT	    /api/posts/<id>	Update a post by ID
DELETE	/api/posts/<id>	Delete a post by ID
GET	    /api/posts/search	Search posts by title or content
## Sorting and Searching
- ### Sorting:
Add query parameters, e.g. /api/posts?sort=title&direction=desc

- ### Search:
/api/posts/search?title=flask&content=python

## Swagger Documentation
API documentation is available at /api/docs

Swagger JSON file is located at /static/masterblog.json and must be present for the docs to load

## Troubleshooting
If masterblog.json is not found, ensure it is placed in the static folder at the root of the repo

Always run Flask from the repo root, not a subdirectory