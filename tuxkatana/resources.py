from importlib.resources import files

import tuxkatana

_params_path = files(tuxkatana).joinpath("params")


def get_resource_file_path(resource_name: str) -> str:
    return _params_path.joinpath(resource_name)
