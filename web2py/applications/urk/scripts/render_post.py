import requests, json, re, os
from jinja2 import Environment, FileSystemLoader

def render_page(api_url, payload, template_file):
    # Fetch the data from the API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    data = {}
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error occurred: {response.status_code}")
        return

    # Load templates
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    # Load the specific template
    template = env.get_template(template_file)

    # Generate and save an HTML page for each post
    for post in data['list']['items']:
        if (post.get('choice5') != 'Published'):
            continue
        # Generate HTML
        output = template.render(post=post)
        post_title = post['title'] # ensure your post object has a 'title'
        post['postContent'] = bytes(post['postContent'], 'utf-8').decode('utf-8', 'ignore')
        # Save to a HTML file
        filename = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', post_title.lower()))[:70] + '.html'
        with open("../static/post/"+filename, 'w+',encoding='utf-8') as file:
            file.write(output)


api_url = 'https://makelist.io/default/call/json/getListView'

payload = {
    "viewName": "allItems",
    "permissionid": "833bed61c64549779640cab51a696a95"
}

render_page(api_url,payload,"post_template.html")

