from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

# Swagger UI configuration
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/Masterblog-API/static/masterblog.json"



swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'  # Displayed app name in Swagger UI
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    valid_sort_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400
    if direction and direction not in valid_directions:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    posts_to_return = POSTS.copy()

    if sort_field:
        reverse = (direction == 'desc')
        posts_to_return.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(posts_to_return)

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    title = data.get('title')
    content = data.get('content')
    missing_fields = []
    if not title:
        missing_fields.append("title")
    if not content:
        missing_fields.append("content")
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Generate new unique ID
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": title,
        "content": content,
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    POSTS = [post for post in POSTS if post['id'] != post_id]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Update title and content if provided, else keep existing
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])

    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    def matches(post):
        return (title_query in post['title'].lower() if title_query else True) and \
               (content_query in post['content'].lower() if content_query else True)

    results = [post for post in POSTS if matches(post)]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
