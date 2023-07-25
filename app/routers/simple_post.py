from fastapi import FastAPI, Response, status, HTTPException, APIRouter

router = APIRouter()

my_posts = [{"id":1, "title": "title of post 1", "content": "content of post 1", "published": True, "rating": 9},
            {"id":2, "title": "title of post 2", "content": "content of post 2", "published": True, "rating": 9}]

# ROOT
@router.get("/")
def root():
    # Add "docs" or "redocs" to access documentation
    return {"detail": "Welcome"}

# CREATE POSTS
@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(item: Post):
    item_dict = item.dict()
    item_dict["id"] = my_posts[-1]["id"] + 1
    item_dict["title"] = item_dict["title"] + f" {item_dict['id']}"
    item_dict["content"] = item_dict["content"] + f" {item_dict['id']}"

    my_posts.routerend(item_dict)
    return {"data": item_dict}

# GET POSTS
@router.get("/posts")
def get_posts():
    return {"data": my_posts}

# GET ONE POST
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@router.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f' post with id: {id} was not found'}
    return {"data": post}

# DELETE ONE POST
def find_index_post(id):
    for idx, post in enumerate(my_posts):
        if post['id'] == id:
            return idx

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_post(id: int):
    idx = find_index_post(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@router.put("/posts/{id}")
def update_one_post(id: int, post: Post):
    idx = find_index_post(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[idx] = post_dict
    return {"data": post_dict}


