from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", context={"posts": posts, "title": "Bloggeur"})


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK,include_in_schema=False)
def post_detail(request: Request, post_id: int):
    for post in posts:
        if post.get('id') == post_id:
            title = post["title"][:20]
            return templates.TemplateResponse(
                request,
                "post.html",
                context={"post": post, "title": title},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 




#  -------------------------API route --------------------------------
@app.get("/api/posts")
def get_posts():
    return posts 


@app.get("/api/posts/{post_id}", status_code=status.HTTP_200_OK)
def get_post_api(post_id: int):
    for post in posts:
        if post.get('id') == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 
