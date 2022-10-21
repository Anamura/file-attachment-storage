import os
import storage


def file_exist(filepath):
    """
    check if file uploaded
    """
    if os.path.exists(filepath):
        return True

    return False


def rename(sign_data, file):
    """
    if user is allowed
    """
    if sign_data is not None:
        return True


def file_path(filepath):
    temp_folder = storage.remote_path
    return os.path.join(temp_folder, filepath[:2], filepath)
