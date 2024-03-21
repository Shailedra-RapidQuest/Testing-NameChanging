import requests, json, re, os
from jinja2 import Environment, FileSystemLoader
from url_safe_image_name import url_safe_image_name

def get_slider_images(product):
    ##if urls already available by file download the return those
    if "slider_image_urls" in product and len(product["slider_image_urls"])>1:
        return product["slider_image_urls"]

    ## if file not uploaded. urls in text boxes

    slider_images = []
    for key, value in product.items():
        if key.startswith('slider_image') and value:
            slider_images.append(value)
    return slider_images


def download_image(url, filename):
        response = requests.get(url)
        # response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(response.content)

def downloadSliderImages(product):  
    folder_name = "../static/assets/img/products/"+product["_id"]

    # Check if folder exists, if not create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    product["slider_image_urls"] = []
    # # Iterate through product dictionary keys and download images
    for key, value in product.items():
        if key.startswith("slider_image") and key.endswith("_file"):
            #image_name = os.path.basename(value)
            try:
                fileId = value["fileId"]
            except:
                continue

            fileUrl = "https://makelist.io"+ value["fileId"]
            fileName = url_safe_image_name(value["fileName"])
         
            save_path = os.path.join(folder_name, fileName)

            download_image(fileUrl, save_path)

            product["slider_image_urls"].append("/assets/img/products"+product["_id"]+"/"+fileName)

    return


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
    for product in data['list']['items']:
        # Generate HTML
 
        downloadSliderImages(product)
  
        product['slider_images'] = get_slider_images(product)

        if "productFile" in product and product["productFile"]:
            base_url = "https://makelist.io"
            product["productFileUrl"] = base_url + product["productFile"]['fileId']

        output = template.render(product=product)
        url_slug = product['url-slug'] # ensure your post object has a 'title'
   
        # Save to a HTML file
        filename = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', url_slug.lower()))[:70] + '.html'
        with open("../static/products/"+filename, 'w+',encoding='utf-8') as file:
            file.write(output)


api_url = 'https://makelist.io/default/call/json/getListView'

payload = {
    "viewName": "allItems",
    "permissionid": "b6b37723ae5d47fca949e7b54861eaea"
}

render_page(api_url,payload,"product_template.html")

