"""
Make conferatur available through a rudimentary JSON-RPC_ interface

.. _JSON-RPC: https://www.jsonrpc.org

"""

import jsonrpcserver
from conferatur import __meta__
from conferatur.normalisation import core, name_to_normaliser, available_normalisers
from functools import wraps
from conferatur.docblock import format_docs
import inspect
import os


def get_methods():
    methods = jsonrpcserver.methods.Methods()

    def method(f, name=None):
        if name is None:
            name = f.__name__.lstrip('_').replace('_', '.')

        methods.add(**{name: f})

    @method
    def version():
        """
        Get the version of conferatur

        :return str: Conferatur version
        """

        return __meta__.__version__

    normalisers = available_normalisers()

    @method
    def normalisation_list():
        """
        Get a list of available core normalisers

        :return object: With key being the normaliser name, and value its description
        """
        return {name: conf.docs
                for name, conf in normalisers.items()}

    def is_safe_path(path):
        return os.path.abspath(path).startswith(os.path.abspath(os.getcwd()))

    class SecurityError(ValueError):
        pass

    def serve_normaliser(config):
        cls = config.cls

        @wraps(cls)
        def _(text, *args, **kwargs):
            # only allow files from cwd to be used...
            if 'file' in kwargs:
                if not is_safe_path(kwargs['file']):
                    raise SecurityError("Access to unallowed file attempted")

            if 'path' in kwargs:
                if not is_safe_path(kwargs['path']):
                    raise SecurityError("Access to unallowed directory attempted")

            return cls(*args, **kwargs).normalise(text)

        # copy signature from original normaliser
        sig = inspect.signature(cls)
        params = [inspect.Parameter('text', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        params.extend(sig.parameters.values())
        sig = sig.replace(parameters=params)
        # todo (?) add available files and folders as select options 
        _.__signature__ = sig
        _.__doc__ += '\n    :param str text: The text to normalise'
        return _

    # add each normaliser as its own api call
    for conf in normalisers.values():
        method(serve_normaliser(conf), name='normalisation.%s' % (conf.name,))

    @method
    def _help():
        """
        Returns available api methods

        :return object: With key being the method name, and value its description
        """

        return {name: format_docs(func.__doc__)
                for name, func in methods.items.items()}

    return methods
