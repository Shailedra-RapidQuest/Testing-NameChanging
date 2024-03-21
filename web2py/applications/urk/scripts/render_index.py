import requests, json, re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os
from url_safe_image_name import url_safe_image_name

def urlify(s):
    s = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', s.lower()))[:70]
    return s

def format_date(s):
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%B %d")


def getListData(api_url,payload):
    # Fetch the data from the API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    data = {}
    if response.status_code == 200:
        data = response.json()
        #allPosts = response.json()["list"]["items"]
        all_templates =  data["list"]["items"]
        return all_templates
    else:
        print(f"Error occurred: {response.status_code}")
        return


def render_page(template_file):
    api_url='https://makelist.io/default/call/json/getListView'
    payload = {
        "viewName": "allItems",
        "permissionid": "b6b37723ae5d47fca949e7b54861eaea"
    }
    all_templates = getListData(api_url,payload)


    ##get categories list
    api_url='https://makelist.io/default/call/json/getListView'
    payload = {
        "viewName": "allItems",
        "permissionid": "a4c39b15aad449f6b374273b6a89189b"
    }
    all_categories = getListData(api_url,payload)


    # Load templates
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.filters['urlify'] = urlify
    env.filters['format_date'] = format_date


    # Load the specific template
    template = env.get_template(template_file)


    ## Get recent templates
    recent_templates = all_templates[-12:]

    for product in recent_templates:
        if "slider_image1_file" in product:
            image_name = product["slider_image1_file"]["fileName"]
            image_name = url_safe_image_name(image_name)
            product_id = product.get("_id","default")
            product["preview_image"] = "/assets/img/products/" + product_id + "/previews/"+  image_name
            #product["slider_image1"] = "https://makelist.io"+product["slider_image1_file"]["fileId"]

    filtered_categories = []
    for category in all_categories:
        if "DisplayONHomePage" in category and category["DisplayONHomePage"] == "Yes":
           filtered_categories.append(category)

    # Generate HTML
    output = template.render(recent_templates=recent_templates,all_categories=filtered_categories)
    
    return output

def save_to_file(filename, content):
    # Save to a HTML file
    with open(filename, 'w') as file:
        file.write(content)



index_html = render_page('homepage_template.html')
save_to_file('../static/index.html', index_html)
