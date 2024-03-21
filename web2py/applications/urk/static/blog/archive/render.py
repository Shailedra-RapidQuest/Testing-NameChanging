import requests, json
from jinja2 import Environment, FileSystemLoader


url = 'https://makelist.io/default/call/json/getListView'

payload = {
    "viewName": "allItems",
    "permissionid": "833bed61c64549779640cab51a696a95"
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    allPosts = response.json()["list"]["items"]
    print(allPosts)
else:
    print(f"Error occurred: {response.status_code}")

# data = response.json()

# Load templates
file_loader = FileSystemLoader('templates')  # assuming templates are in a directory named "templates"
env = Environment(loader=file_loader)

# Load the specific template
template = env.get_template('blog_template.html')

# Generate HTML
output = template.render(allPosts=allPosts)

# Save to a HTML file
with open('index.html', 'w') as file:
    file.write(output)
