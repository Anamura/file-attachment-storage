from aiohttp.web_response import json_response
import aiohttp_swagger
from flask import session, redirect, render_template,  request
from aiohttp import web
from storage import storage
from logger import get_default_logger
from flask_swagger_ui import get_swaggerui_blueprint

user = {"username": "", "password": ""}
logger = get_default_logger("WEB_APP")

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': ''
    }
)
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def routes(application):
    application.router.add_route('POST', '/api/files/upload', upload_file)
    application.router.add_route('DELETE', '/api/files/delete/{hash}', delete)
    application.router.add_route('GET', '/api/files/download/{hash}', download_file)


async def upload_file(request):
    reader = await request.multipart()
    file = await reader.next()

    hash_f = await storage.upload(file)
    return json_response({'hash': hash_f})


def delete(path):
    try:
        auth_header = path.headers["Authorization"]
        if auth_header:
            hash_f = path.match_info.get('hash', None)
            storage.delete_file(hash_f)
            return json_response('OK',  status=200)
    except KeyError:
        response = {'code': 401, 'message': 'Authorization is missing or invalid.'}
        return json_response(response, status=401)


async def download_file(path):
    hash_f = path.match_info.get('hash', None)
    if hash_f is not None:
        return await storage.download(hash_f)


def login():
    if request.method == 'POST':
        if session.get('logged_in'):
            session['user'] = request.form.get('username')
    return render_template('')


def logout():
    session.pop('user')
    return redirect('/login')


if __name__ == "__main__":
    logger.info("Starting app")
    # app.run()
    app = web.Application()
    routes(app)
    aiohttp_swagger.setup_swagger(app, swagger_from_file='../../../../file-attachment-storage/static/swagger.yaml',  swagger_url="/api/docs")
    web.run_app(app, host='127.0.0.1', port=5000)