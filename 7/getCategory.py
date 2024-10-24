from urllib.parse import urlparse

def get_category(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Remove leading slash if present
    if path.startswith("/"):
        path = path[1:]

    # Extract the desired part
    desired_part = path.split("/")[0]

    return desired_part