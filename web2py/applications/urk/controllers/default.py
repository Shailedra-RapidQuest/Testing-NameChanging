# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

import asyncio
import json
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()
Personal_Access_Token = os.getenv("Personal_Access_Token")
Current_Path = os.getenv("Current_Path")
Branch_Name = os.getenv("Branch_Name")
# ---- example index page ----


def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


@request.restful()
def testing():
    def GET(*args, **kwargs):
        return "API is Working Successfully..."
    return locals()


@request.restful()
def render_page():
    def GET(*args, **kwargs):
        try:
            asyncio.run(render_script_file())
            return "Script run successfully."
        except Exception as e:
            return "Error while running the script: " + str(e)

    return locals()


async def render_script_file():
    await asyncio.create_subprocess_exec('python3', 'test.py', cwd=Current_Path+"/web2py/applications/urk/scripts")
    # await asyncio.create_subprocess_exec('python3', 'runAll.py', cwd=Current_Path+"/web2py/applications/urk/scripts/")


@request.restful()
def git_webhook():
    def POST(*args, **kwargs):
        try:
            print("Webhook running sucessfully...")
            payload = json.loads(request.body.read().decode('utf-8'))
            branch = payload.get('ref', '').split('/')[-1]
            print(branch)
            if branch == Branch_Name:
                result = subprocess.run(['git', 'pull', Personal_Access_Token, Branch_Name],
                                        capture_output=True, text=True, cwd=Current_Path)
                print("result", result)
                if result.returncode == 0:
                    response_text = "Git pull successful"
                else:
                    response_text = "Error during git pull:\n" + result.stderr
            else:
                response_text = f"Push event not from"+Branch_Name
            return response_text

        except Exception as e:
            return "Error during git pull: " + str(e)

    return locals()

# ---- API (example) -----


@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET':
        raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})

# ---- Smart Grid (example) -----


# can only be accessed by members of admin groupd
@auth.requires_membership('admin')
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:
        raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[
                             tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----


def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
