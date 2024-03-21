import requests, json, re, os
from jinja2 import Environment, FileSystemLoader
from url_safe_image_name import url_safe_image_name

def download_and_save_image(url, save_path):
    """
    Download an image from the given URL and save it to the specified path.
    """
    # Ensure the directory exists

    if not os.path.exists(save_path):
        # Ensure the directory exists
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print("file already exists... continue",save_path)


def get_slider_images(product):
    ##if urls already available by file download the return those
    slider_images = []

    base_url = "https://makelist.io"
    product_id = product.get('_id', 'default_id')
    static_folder = "../static/assets/img/products/"

    if "slider_image1_file" in product:

        for key, value in product.items():
            if key.startswith('slider_image') and key.endswith("_file"):
                try:
                    fileId = value["fileId"]
                except:
                    continue

                image_name = value.get("fileName", "default_image.PNG")
                image_name = url_safe_image_name(image_name)
                # Construct the URL to download the image
                download_url = base_url + value["fileId"]
                # Construct new static path
                new_path = static_folder + "/" + product_id + "/previews/"+ image_name


                # Download and save the image to the new path
                download_and_save_image(download_url, new_path)
                
                #slider_images.append("https://makelist.io"+value["fileId"])
                img_path = "/assets/img/products/" + product_id + "/previews/"+ image_name
                slider_images.append(img_path)
                

        return slider_images
    else:
        print("No uploaded file in slider using old algo")

        # if "slider_image_urls" in product and len(product["slider_image_urls"])>1:
        #     print("Returning item[slider_image_urls]",product["slider_image_urls"])
        #     return product["slider_image_urls"]


        ## if file not uploaded. urls in text boxes

        slider_images = []
        for key, value in product.items():
            if key.startswith('slider_image') and value:
                slider_images.append(value)
        return slider_images




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

