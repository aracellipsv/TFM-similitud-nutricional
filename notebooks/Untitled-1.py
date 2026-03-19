
import requests

API_KEY = "BomzyXHp675ljuSka2IlT3s8wc4Bv1x1nVyhh1rb"
BASE_URL = "https://api.nal.usda.gov/fdc/v1"

response = requests.get(
    f"{BASE_URL}/foods/search",
    params={
        "api_key": API_KEY,
        "query": "breakfast cereal",
        "dataType": ["Branded"],
        "pageSize": 5
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Conexión exitosa")
    print(f"Total productos: {data['totalHits']}")
    for food in data['foods']:
        print(f"  - {food['description']}")
else:
    print(f"Error: {response.status_code}")