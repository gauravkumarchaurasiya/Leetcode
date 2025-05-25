from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os, json
from datetime import datetime

app = FastAPI()

# Create directories if they don't exist
os.makedirs("frontend/data", exist_ok=True)
os.makedirs("frontend/images", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Serve index.html at root
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/add-blog")
async def blog_form(request: Request):
    return templates.TemplateResponse("blog_form.html", {"request": request})

@app.get("/add-post")
async def post_form(request: Request):
    return templates.TemplateResponse("post_form.html", {"request": request})

@app.post("/submit-blog")
async def submit_blog(
    leetcode_id: str = Form(...),
    title: str = Form(...),
    tags: str = Form(...),
    python_solution: str = Form(...)
):
    blog_data = {
        "leetcode_id": leetcode_id,
        "title": title,
        "tags": [tag.strip() for tag in tags.split(",")],
        "python_solution": python_solution
    }

    blogs_file = "frontend/data/blogs.json"
    blogs = []
    if os.path.exists(blogs_file):
        with open(blogs_file, "r") as f:
            blogs = json.load(f)
    
    blogs.insert(0, blog_data)
    with open(blogs_file, "w") as f:
        json.dump(blogs, f, indent=2)

    return RedirectResponse(url="/static/blog.html", status_code=302)

# @app.post("/submit-post")
# async def submit_post(
#     leetcode_ids: str = Form(...),
#     description: str = Form(...),
#     tags: str = Form(...),
#     images: list[UploadFile] = File(...)
# ):
#     image_names = []
#     for image in images:
#         if image.filename:
#             path = os.path.join("frontend/images", image.filename)
#             with open(path, "wb") as buffer:
#                 shutil.copyfileobj(image.file, buffer)
#             image_names.append(image.filename)

#     post_data = {
#         "date": datetime.now().strftime("%Y-%m-%d"),
#         "leetcode_ids": [id.strip() for id in leetcode_ids.split(",")],
#         "description": description,
#         "tags": [tag.strip() for tag in tags.split(",")],
#         "images": image_names
#     }

#     posts_file = "frontend/data/posts.json"
#     posts = []
#     if os.path.exists(posts_file):
#         with open(posts_file, "r") as f:
#             posts = json.load(f)

#     posts.insert(0, post_data)
#     with open(posts_file, "w") as f:
#         json.dump(posts, f, indent=2)

#     return RedirectResponse(url="/static/index.html", status_code=302)

@app.post("/submit-post")
async def submit_post(
    leetcode_ids: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),
    images: list[UploadFile] = File(...)
):
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    
    post_data = {
        "date": today,
        "leetcode_ids": [id.strip() for id in leetcode_ids.split(",")],
        "description": description,
        "tags": [tag.strip() for tag in tags.split(",")],
        "images": []
    }

    # Process images
    for image in images:
        if image.filename:
            # Add timestamp to filename to make it unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{image.filename}"
            path = os.path.join("frontend/images", safe_filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            post_data["images"].append(safe_filename)

    # Load existing posts
    posts_file = "frontend/data/posts.json"
    posts = []
    if os.path.exists(posts_file):
        with open(posts_file, "r") as f:
            posts = json.load(f)

    # Check if post for today already exists
    today_post = next((post for post in posts if post["date"] == today), None)
    if today_post:
        # Update existing post
        today_post["leetcode_ids"].extend(post_data["leetcode_ids"])
        today_post["description"] += f"\n\nUpdate:\n{post_data['description']}"
        today_post["tags"].extend(post_data["tags"])
        today_post["images"].extend(post_data["images"])
    else:
        # Add new post
        posts.insert(0, post_data)

    # Save updated posts
    with open(posts_file, "w") as f:
        json.dump(posts, f, indent=2)

    return RedirectResponse(url="/static/index.html", status_code=302)