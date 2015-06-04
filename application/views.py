import requests

from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    current_app,
    make_response,
    redirect,
)

from ukpostcodeutils.validation import is_valid_postcode as full
from ukpostcodeutils.validation import is_valid_partial_postcode as partial

from application.utils import log_traceback

from urllib.parse import quote

application = Blueprint('application', __name__)


def get_address(location):
    try:
        address = location['entry']['address'].split(':')[-1]
        url = '%s/address/%s' % (current_app.config['ADDRESS_REGISTER'], address)
        current_app.logger.info('Get address from ' + url)
        params = {"_representation": "json"}
        res = requests.get(url, params=params)
        current_app.logger.info(res.json())
        return res.json()
    except Exception as e:
        return {"hash": "", "entry": {"address": "not found"}}


def get_postcode(address):
    try:
        postcode = address['entry']['postcode']
        current_app.logger.info(postcode)
        postcode_url_safe = quote(postcode, safe='')
        url = '%s/postcode/%s' % (current_app.config['POSTCODE_REGISTER'], postcode_url_safe)
        current_app.logger.info('Get postcode from ' + url)
        params = {"_representation": "json"}
        res = requests.get(url, params=params)
        current_app.logger.info(res.json())
        return res.json()
    except Exception as e:
        return {"hash": "", "entry": {"postcode": postcode}}

# def get_posttown(address):
#     try:
#         posttown = address['entry']['post-town'].title()
#         posttown_url_safe = quote(posttown, safe='')
#         url = '%s/post-town/%s' % (current_app.config['POSTTOWN_REGISTER'], posttown_url_safe)
#         current_app.logger.info('Get post town from ' + url)
#         params = {"_representation": "json"}
#         res = requests.get(url, params=params)
#         current_app.logger.info(res.json())
#         return res.json()
#     except Exception as e:
#         return {"hash": "", "entry": {"post-town": posttown}}


def is_postcode_search(query):
    query = query.replace(' ', '').upper()
    return full(query) or partial(query)


# hokey search by postcode. too many requests
def lookup_by_address_id(postcode):
    url = '%s/search' % current_app.config['ADDRESS_REGISTER']
    params = {'_query': postcode, "_representation": "json"}
    res = requests.get(url, params=params)
    address_ids = [item['entry']['address'] for item in res.json()]
    entries = []
    for id in address_ids:
        params = {"_representation": "json"}
        url = '%s/address/%s' % (current_app.config['SCHOOL_REGISTER'], id)
        res = requests.get(url, params=params)
        if res.status_code == 200:
            entries.append(res.json())

    return render_template('results.html', entries=entries)


# govuk_template asset path
@application.context_processor
def asset_path_context_processor():
    return {'asset_path': '/static/'}


@application.route('/')
def index():
    postback = request.args.get('postback')
    response = make_response(render_template('index.html'))
    if postback:
        response.set_cookie('postback', postback)
    else:
        response.set_cookie('postback')

    return response


@application.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        abort(400)

    if is_postcode_search(query):
        return lookup_by_address_id(query)
    else:
        params = {"_query": query, "_representation": "json"}
        url = '%s/search' % current_app.config['SCHOOL_REGISTER']
        try:
            res = requests.get(url, params=params)
            res.raise_for_status
            current_app.logger.info(res.json())
            return render_template('results.html', entries=res.json())
        except Exception as e:
            log_traceback(current_app.logger, e)
            return render_template('results.html', entries=[])


@application.route('/location/<id>')
def location(id):
    params = {"_representation": "json"}
    url = '%s/school/%s' % (current_app.config['SCHOOL_REGISTER'], id)
    try:
        res = requests.get(url, params=params)
        res.raise_for_status
        location = res.json()
        current_app.logger.info(location)
        address = get_address(location)
        if address:
            postcode = get_postcode(address)
            #posttown = get_posttown(address)
            address_register = current_app.config['ADDRESS_REGISTER']
            location_register = current_app.config['SCHOOL_REGISTER']
            postcode_register = current_app.config['POSTCODE_REGISTER']
            #posttown_register = current_app.config['POSTTOWN_REGISTER']
            postback = request.cookies.get('postback')
            return render_template('location.html', location=location, address=address,
                                   postcode=postcode,
                                   location_register=location_register,
                                   address_register=address_register,
                                   postcode_register=postcode_register,
                                   postback=postback,
                                   id=id)
        else:
            abort(404)
    except Exception as e:
        log_traceback(current_app.logger, e)
        return abort(res.status_code)

@application.route('/postback/<id>')
def postback(id):
    postback = request.cookies.get('postback')
    response = redirect('%s/%s' % (postback, id))
    response.set_cookie('postback')
    return response
