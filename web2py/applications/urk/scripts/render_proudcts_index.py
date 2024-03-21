import requests, json, re, os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from url_safe_image_name import url_safe_image_name

def format_date(s):
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%B %d")



def render_page(api_url,payload,template_file):
    # Fetch the data from the API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    data = {}
    if response.status_code == 200:
        data = response.json()
        #allPosts = response.json()["list"]["items"]
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

    for product in data['list']['items']:
        # Generate HTML
        if "slider_image1_file" in product:
            #product["slider_image1"] = "https://makelist.io"+product["slider_image1_file"]["fileId"]
            image_name = product["slider_image1_file"]["fileName"]
            image_name = url_safe_image_name(image_name)
            product_id = product.get("_id","default")
            product["preview_image"] = "/assets/img/products/" + product_id + "/previews/"+  image_name
    
        else:
            preview_image = 'slider_image1_file_missing'

    # Generate HTML

    output = template.render(data=data)
    
    return output

def save_to_file(filename, content):
    # Save to a HTML file
    with open(filename, 'w') as file:
        file.write(content)


payload = {
    "viewName": "allItems",
    "permissionid": "b6b37723ae5d47fca949e7b54861eaea"
}
product_html = render_page('https://makelist.io/default/call/json/getListView',payload,'products-index.html')
save_to_file('../static/products/index.html', product_html)
