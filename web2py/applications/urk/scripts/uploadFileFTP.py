from ftplib import FTP, error_perm
import os
from datetime import datetime, timedelta
import os
 
# Define your FTP connection parameters
host = 'rapidquest.in'
port = 21  # Default FTP port; might be different for your setup
username = 'uploadscript@ultimateresourcekit.com'
password = 'Y5rOlXL2gudL'


# Connect to the FTP server
ftp = FTP()
ftp.connect(host, port)
ftp.login(username, password)


#Function to ensure directory exists
def directory_exists(ftp, dir_name):
    """
    Check if a directory exists on the FTP server.
    """
    try:
        # List the contents of the current directory
        listing = ftp.nlst()

        # Check if the desired directory is in the listing
        return dir_name in listing
    except error_perm as e:
        # Handle common FTP errors, like no permission to list directory
        print(f"FTP error: {e}")
        return False

        

def uploadFile(local_file_path,remote_dir,fileName):
    # Upload the file
    print("uploading...",local_file_path,remote_dir,fileName)
    
    # Usage example:
    if not directory_exists(ftp, remote_dir):
        #ftp.mkd(remote_dir)
        pass

    ftp.cwd(remote_dir)
    print("saving to", remote_dir)

    with open(local_file_path, 'rb') as local_file:
        ftp.storbinary('STOR ' + fileName, local_file)

    ftp.cwd("/")


#Upload Index.html, custom.css
local_file_path = '../static/index.html'
fileName = 'index.html'
remote_dir = "."
uploadFile(local_file_path,remote_dir,fileName)

local_file_path = '../static/sitemap.xml'
fileName = 'sitemap.xml'
remote_dir = "."
uploadFile(local_file_path,remote_dir,fileName)



local_file_path = '../static/assets/css/custom.css'
fileName = 'custom.css'
remote_dir = "assets/css/"
uploadFile(local_file_path,remote_dir,fileName)
########################



##Upload All Product Categories

local_directory = '../static/category/'
remote_dir = "/category/"

for filename in os.listdir(local_directory):
    local_path = os.path.join(local_directory, filename)    
    if os.path.isfile(local_path):
        uploadFile(local_path,remote_dir,filename)


##########################
# upload all products 


local_file_path = '../static/products/index.html'
fileName = 'index.html'
remote_dir = "products"
uploadFile(local_file_path,remote_dir,fileName)

## upload all products 

local_directory = '../static/products/'

for filename in os.listdir(local_directory):
    local_path = os.path.join(local_directory, filename)    
    if os.path.isfile(local_path):
        
        uploadFile(local_path,remote_dir,filename)



##Close the FTP connection
ftp.quit()

os.system(".\\backup\\mongodump.exe --uri mongodb+srv://backup-script:a4j4RpvsWXLl9pYo@cluster0.63azr.mongodb.net/ultimate-resource-kit")
