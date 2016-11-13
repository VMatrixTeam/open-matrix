from handlers.user.profile import ProfileHandler

urls = [
    (r'/profile/(.*)', ProfileHandler)
]
