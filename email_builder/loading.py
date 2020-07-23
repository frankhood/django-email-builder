import sys
import traceback


class ClassNotFoundError(Exception):
    pass


def _import_module(module_path, classname):
    """ Tries to import the given Python module path. """
    try:
        imported_module = __import__(module_path, fromlist=[classname])
        return imported_module
    except ImportError:
        # In case of an ImportError, the module being loaded generally does not exist. But an
        # ImportError can occur if the module being loaded exists and another import located inside
        # it failed.
        #
        # In order to provide a meaningfull traceback, the execution information can be inspected in
        # order to determine which case to consider. If the execution information provides more than
        # a certain amount of frames, this means that an ImportError occured while loading the
        # initial Python module.
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        if len(frames) > 1:
            raise


def _pick_up_class(module, classname):
    """ Given a list of class names to retrieve, try to fetch them from the specified list of
        modules and returns the list of the fetched classes.
    """
    klass = None
    if hasattr(module, classname):
        klass = getattr(module, classname)
    if not klass:
        raise ClassNotFoundError("Error fetching '{}' in {}".format(classname, str(module.__name__)))
    return klass
