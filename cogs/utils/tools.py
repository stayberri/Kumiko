import discord


def get_friendly_avatar(user, replace_webp=True):
    """Returns a user friendly avatar url.
    This is done by replacing the size on gifs so that they can animate and if replace_webp is True (True by Default)
    .webp images are replaced with .png"""
    url = user.avatar_url
    url = url.replace("gif?size=1024", "gif")
    if replace_webp is True:
        url = url.replace(".webp", ".png")
    return url
