from util.config_util import CONFIG

def save_from_file(file):
    file_name = file.filename
    file_path = f'{CONFIG.path.inputPath}/videos/{file_name}'
    print(file_path)
    file.save(file_path)

    return file_path