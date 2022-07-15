from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    fullname: str
    birthday: str
    mail: str
    faculty: str
    course: str
    mark: str
    fulltime_or_remote: str
    city: str


while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', port = '5432', user = 'postgres', 
                            password = '12122001', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#     {"title": "favourite foods", "content": "I like pizza", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM "Students" """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO "Students" (fullname, birthday, mail, faculty, course, mark, fulltime_or_remote, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING
     * """,
                   (post.fullname, post.birthday, post.mail, post.faculty, post.course, post.mark, post.fulltime_or_remote, post.city))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * from "Students" WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return {"post_detail": post}
    

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM "Students" WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()  
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE "Students" SET fullname = %s, birthday = %s, mail = %s, 
    faculty = %s, course = %s, mark = %s, fulltime_or_remote = %s, city = %s WHERE id = %s RETURNING *""",
    
                    (post.fullname, post.birthday, post.mail, post.faculty, post.course, post.mark, post.fulltime_or_remote, 
                    post.city, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")

    return{"data": updated_post}


# @app.patch("/posts/{id}")
# def update_post(id: int, post: Post):

#     cursor.execute("""UPDATE "Students" SET fullname = %s, birthday = %s, mail = %s WHERE id = %s RETURNING *""",
    
#                     (post.fullname, post.birthday, post.mail, str(id)))

#     updated_post = cursor.fetchone()
#     conn.commit()

#     if updated_post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} does not exist")

#     return{"data": updated_post}
