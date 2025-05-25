from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import os

app = FastAPI()

# Folders where posts/blogs will be saved
POSTS_DIR = "./_posts"
BLOGS_DIR = "./_blogs"

# Ensure directories exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(BLOGS_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    # Simple filename sanitizer: lowercase, replace spaces with dashes, remove special chars
    import re
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\- ]", "", name)
    name = name.replace(" ", "-")
    return name

def create_markdown_post(title, tags, code, explanation, screenshot=None):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{sanitize_filename(title)}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    tags_str = ", ".join([tag.strip() for tag in tags.split(",")]) if tags else ""

    front_matter = f"""---
layout: post
title: "{title}"
date: {date_str}
tags: [{tags_str}]
screenshot: {screenshot if screenshot else ''}
---

"""

    content = front_matter + explanation + "\n\n```python\n" + code + "\n```\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def create_markdown_blog(title, tags, code, explanation):
    # Similar to post but saved in blogs folder, no screenshot
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{sanitize_filename(title)}.md"
    filepath = os.path.join(BLOGS_DIR, filename)

    tags_str = ", ".join([tag.strip() for tag in tags.split(",")]) if tags else ""

    front_matter = f"""---
layout: blog
title: "{title}"
date: {date_str}
tags: [{tags_str}]
---

"""

    content = front_matter + explanation + "\n\n```python\n" + code + "\n```\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head>
            <title>LeetCode Post & Blog Creator</title>
        </head>
        <body>
            <h2>Create LeetCode Post & Blog</h2>
            <form action="/" method="post">
                <label>Question Title:</label><br>
                <input type="text" name="title" required size="60"><br><br>
                
                <label>Tags (comma separated):</label><br>
                <input type="text" name="tags" size="60"><br><br>
                
                <label>Code (Python):</label><br>
                <textarea name="code" rows="10" cols="70" required></textarea><br><br>
                
                <label>Explanation / Solution:</label><br>
                <textarea name="explanation" rows="10" cols="70" required></textarea><br><br>
                
                <label>Screenshot Path (optional):</label><br>
                <input type="text" name="screenshot" size="60" placeholder="/assets/screenshots/example.png"><br><br>
                
                <input type="submit" value="Create Post & Blog">
            </form>
        </body>
    </html>
    """

@app.post("/", response_class=RedirectResponse)
async def submit_form(
    title: str = Form(...),
    tags: str = Form(""),
    code: str = Form(...),
    explanation: str = Form(...),
    screenshot: str = Form(None),
):
    create_markdown_post(title, tags, code, explanation, screenshot)
    create_markdown_blog(title, tags, code, explanation)
    return RedirectResponse(url="/", status_code=303)
