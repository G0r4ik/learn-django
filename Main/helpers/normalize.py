def normalizeUser(user):
    return {"id": user["id"], "email": user["email"], "username": user["username"]}


def normalizePost(user, post):
    normalizePost = {
        "title": post.title,
        "text": post.text,
        "date": post.date,
        "postID": post.post_id or post.id,
        "user": normalizeUser(user),
    }
    return normalizePost
