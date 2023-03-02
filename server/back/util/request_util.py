from util.config_util import CONFIG

def is_allowed_image_format(file_name):
    if not file_name:
        return False
    return '.' in file_name and file_name.rsplit('.', 1)[1] in CONFIG.server.back.allowedImageExtensions

def is_allowed_video_format(file_name):
    if not file_name:
        return False
    return '.' in file_name and file_name.rsplit('.', 1)[1] in CONFIG.server.back.allowedVideoExtensions