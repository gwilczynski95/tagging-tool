import os

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
import numpy as np

from tagging_tool import utils

bp = Blueprint("tagging", __name__, url_prefix="/tagging")

portrait_loader = utils.ImageLoader('/home/grzegorz/grzegos_world/15_december_2021/flask/examples/tutorial/flaskr/static/images/portrait')
main_save_path = '/home/grzegorz/projects/museum/cut_images/portrait'

max_x_size = 2000
max_y_size = 700


@bp.route("/")
def index():
    return portrait()


@bp.route("/portrait")
def portrait():
    info = dict()
    info['title'] = 'Portraits'
    image, refactored_path = utils.load_image_with_info(portrait_loader)
    rescaled_x, rescaled_y = utils.rescale_dims(image, max_x_size, max_y_size)

    info['curr_img_path'] = refactored_path
    info['x_size'] = rescaled_x
    info['y_size'] = rescaled_y

    return render_template("tagging/tag.html", value=info)


@bp.route('/cut', methods=['POST'])
def perform_cutting():
    # fixme: should be made differently but right now it's ok
    request_data = eval(request.data)
    # where = request_data['location']
    where_ratio = request_data['location_rat']
    kind = request_data['kind']
    current_path = request_data['curr_path']
    # check if cached image is proper
    if current_path != portrait_loader.current_renamed_path:
        return jsonify(success=False), 404
    portrait_loader.was_current_image_processed = True
    image = np.array(portrait_loader.current_image)

    # calculate pos of checked point
    x_shape = image.shape[1]
    y_shape = image.shape[0]
    x_point = int(where_ratio['x'] * x_shape)
    y_point = y_shape - int(where_ratio['y'] * y_shape)

    # perform cutting
    cut_image = utils.cut_to_square(image, x_point, y_point)
    current_filename = portrait_loader[portrait_loader.current_pos - 1].split('/')[-1]
    temp_path = os.path.join(main_save_path, current_filename)
    utils.save_image(temp_path, cut_image)
    os.remove(portrait_loader[portrait_loader.current_pos - 1])

    return jsonify(success=True), 200
