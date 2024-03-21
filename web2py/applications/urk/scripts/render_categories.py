import requests
import json
import re
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from url_safe_image_name import url_safe_image_name


def urlify(s):
    s = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', s.lower()))[:70]
    return s


def format_date(s):
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%B %d")


def render_page(api_url, payload, template_file, category):
    # Fetch the data from the API
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        api_url, data=json.dumps(payload), headers=headers)
    data = {}
    if response.status_code == 200:
        data = response.json()
        # allPosts = response.json()["list"]["items"]
        # print(data)
    else:
        print(f"Error occurred: {response.status_code}")
        return

    category_products = []
    for product in data['list']['items']:
        if "slider_image1_file" in product:
            image_name = product["slider_image1_file"]["fileName"]
            image_name = url_safe_image_name(image_name)
            product_id = product.get("_id", "default")
            product["preview_image"] = "/assets/img/products/" + \
                product_id + "/previews/" + image_name

            # product["slider_image1"] = "https://makelist.io"+product["slider_image1_file"]["fileId"]

        if "productCategory" in product and product["productCategory"] != {}:
            # check if productCategory Id == categoryId
            if product["productCategory"]["text1"] == category["name"]:
                # print(">>>>>  >>>>",product["productCategory"])
                category_products.append(product)

    print("Here are all products from category", category_products)

    # add to products to category object
    category["products"] = category_products

    # Load templates
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.filters['urlify'] = urlify
    env.filters['format_date'] = format_date

    # Load the specific template
    template = env.get_template(template_file)

    # Generate HTML
    # category = dict(
    #     name = "Employee Handbook",
    #     description = "Discover comprehensive employee handbooks tailored for today's workforce. Our guides cover everything from onboarding processes to company policies, ensuring a well-informed and cohesive team environment. Dive in to find the perfect handbook for your organization.",
    #     shortDescMeta = "Fully Customizable Editable Templates",
    #     url = "https://ultimateresourcekit.com/category/employee-handbook",
    #     keywords = "Employee Handbook Templates, Customizable Employee Handbook Templates, Employee Handbook examples, Staff Handbook template, MS Word Editable Templates",
    #     products = category_products
    # )

    output = template.render(category=category)

    return output


def save_to_file(filename, content):
    # Save to a HTML file
    with open(filename, 'w') as file:
        file.write(content)


categories = [
    {
        "name": "Onboarding Checklist",
        "description": "Our Onboarding Checklist templates are meticulously designed to ensure a smooth and efficient transition for new employees into any organization or team. They serve as a comprehensive roadmap, detailing every essential step from the initial welcome to full integration into the company. These templates are versatile and adaptable, catering to a wide spectrum of industries and organizational structures, ensuring that every new hire can hit the ground running and contribute to the company's success from day one.",
        "shortDescMeta": "Onboarding Checklist Templates | MS Word Templates",
        "url": "https://ultimateresourcekit.com/category/onboarding-checklist",
        "url_slug": "onboarding-checklist",
        "keywords": "Employee Onboarding, Onboarding Checklist Template, New Hire Integration, HR Resources, Employee Induction, Staff Orientation, Onboarding Best Practices, MS Word Editable Templates",
        "products": []
    },
    {
        "name": "Recruitment Dashboard",
        "description": "Our Recruitment Dashboard templates are meticulously designed to monitor, track, and improve the efficiency and effectiveness of the recruitment process. They offer a visual representation of key performance indicators, helping HR professionals and hiring managers to make data-driven decisions. These templates cater to a broad range of industries and organizational structures, ensuring the hiring process aligns with company goals and benchmarks.",
        "shortDescMeta": "Recruitment Dashboard Templates | PowerPoint Templates",
        "url": "https://ultimateresourcekit.com/category/recruitment-dashboard-template",
        "url_slug": "recruitment-dashboard-template",
        "keywords": "hiring dashboard, hiring dashboard template, recruitment metrics dashboard PowerPoint, HR Dashboards, talent acquisition dashboard, recruitment dashboard excel, PowerPoint Dashboard Templates",
        "products": []
    },
    {
        "name": "Employee Handbook",
        "description": "Discover comprehensive employee handbooks tailored for today's workforce. Our guides cover everything from onboarding processes to company policies, ensuring a well-informed and cohesive team environment. Dive in to find the perfect handbook for your organization.",
        "shortDescMeta": "Fully Customizable Editable Templates",
        "url": "https://ultimateresourcekit.com/category/employee-handbook",
        "url_slug": "employee-handbook",
        "keywords": "Employee Handbook Templates, Customizable Employee Handbook Templates, Employee Handbook examples, Staff Handbook template, MS Word Editable Templates",
        "products": []
    }
]

payload = {
    "viewName": "allItems",
    "permissionid": "b6b37723ae5d47fca949e7b54861eaea"
}

for category in categories:
    product_html = render_page(
        'https://makelist.io/default/call/json/getListView', payload, 'category.html', category=category)
    save_to_file('../static/category/' +
                 category['url_slug']+'.html', product_html)
