from django.conf import settings

def build_file_url(path, request=None):
    from django.conf import settings

    media_url = settings.MEDIA_URL

    if not media_url.startswith("/"):
        media_url = "/" + media_url
    if not media_url.endswith("/"):
        media_url = media_url + "/"

    if path.startswith(media_url):
        relative_path = path[len(media_url):]
    elif path.startswith("/"):
        relative_path = path[1:]
    else:
        relative_path = path

    url = f"{media_url}{relative_path}"

    # Ensure single slash after domain
    url = url.replace("//", "/")
    if request:
        abs_url = request.build_absolute_uri(url)
        # Force HTTPS if needed
        if abs_url.startswith("http://"):
            abs_url = abs_url.replace("http://", "https://", 1)
        return abs_url
    return url