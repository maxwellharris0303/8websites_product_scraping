from urllib.parse import urlparse

url = "https://www.123watersport.nl/ankeren-afmeren/afmeren/"
parsed_url = urlparse(url)
path_parts = parsed_url.path.split("/")

try:
    category = path_parts[1]
    subcategory = path_parts[2]
    subsubcategory = path_parts[3]
    subsubcategory1 = path_parts[4]
except:
    pass
try:
    print(category)         # Output: ankeren-afmeren
    print(subcategory)      # Output: afmeren
    print(subsubcategory)   # Output: aanlegringen-meerpennen
    print(subsubcategory1)   # Output: aanlegringen-meerpennen
except:
    pass