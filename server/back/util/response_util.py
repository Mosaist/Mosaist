from flask import jsonify, make_response

import util.image_util as image_util

def response_image(image):
    response = make_response(image_util.to_png_byte(image))
    response.headers.set('Content-Type', 'image/png')
    return response

class ResponseCode:
    BAD_REQUEST = lambda message='Bas request': make_response(jsonify({ 'code': 400, 'message': message }), 400)
    INTERNAL_SERVER_ERROR = lambda message='Internal server error': make_response(jsonify({ 'code': 500, 'message': message }), 500)
    NOT_IMPLEMENTED = lambda message='Not implemented': make_response(jsonify({ 'code': 501, 'message': message }), 501)