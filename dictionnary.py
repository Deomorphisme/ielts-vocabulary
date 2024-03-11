import json
import requests

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    json_data = response.json()[0]["meanings"]
    json_indent = json.dumps(json_data, indent=1)
    table_suppression = str.maketrans("", "", r"{}[]")
    json_sans_accolades = json_indent.translate(table_suppression)
    print(json_sans_accolades)

get_definition('sustain')