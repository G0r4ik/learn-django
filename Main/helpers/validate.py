def validate_username(username):
    if len(username) < 5:
        return "Некоректный лоигн"


def validate_email(email):
    if len(email) < 5:
        return "Некоректная почта"


def validate_password(password):
    if len(password) < 5:
        return "Некоректный пароль"


def validate_title(title):
    if len(title) < 5:
        return "Слишком короткий заголовок"


def validate_text(text):
    if len(text) < 5:
        return "Слишком короткий текст поста"


def validate_comment_text(text):
    if len(text) < 5:
        return "Слишком короткий текст комментария"


def validate_comment_author(author):
    if len(author) < 5:
        return "Слишком короткое имя"
