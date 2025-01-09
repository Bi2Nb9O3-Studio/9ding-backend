import pkgutil
import sys

from flask import Blueprint


app_dict = {}
pkg_list = pkgutil.walk_packages(__path__, __name__ + ".")
built_blueprint=Blueprint("built", __name__)

for _, module_name, ispkg in pkg_list:
    __import__(module_name)
    module = sys.modules[module_name]
    module_attrs = dir(module)
    for name in module_attrs:
      var_obj = getattr(module, name)
      if isinstance(var_obj, Blueprint):
        if app_dict.get(name) is None:
          app_dict[name] = var_obj
          built_blueprint.register_blueprint(var_obj)
