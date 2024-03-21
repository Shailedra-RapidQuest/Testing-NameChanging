import requests
import json
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import json

def urlify(s):
    s = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', s.lower()))[:70]
    return s

def format_date(s):
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%B %d")


def render_page(api_url, payload, template_file):
    # Fetch the data from the API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        api_url, data=json.dumps(payload), headers=headers)
    data = {}
    if response.status_code == 200:
        data = response.json()
        data['list']["items"] = [item for item in data['list']["items"] if item.get('choice5') == 'Published']
    else:
        print(f"Error occurred: {response.status_code}")
        return

    
    # Load templates
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.filters['urlify'] = urlify
    env.filters['format_date'] = format_date

    # Load the specific template
    template = env.get_template(template_file)

    # Generate HTML
    output = template.render(data=data)

    return output


def save_to_file(filename, content):
    # Save to a HTML file
    with open(filename, 'w') as file:
        file.write(content)


payload = {
    "viewName": "allItems",
    "permissionid": "833bed61c64549779640cab51a696a95"
}
blog_html = render_page(
    'https://makelist.io/default/call/json/getListView', payload, 'blog_template.html')
save_to_file('../static/blog/index.html', blog_html)
