"""
Application data stored by virtualenv.
"""
from __future__ import absolute_import, unicode_literals

import logging
import os
from argparse import Action, ArgumentError

from appdirs import user_data_dir

from .na import AppDataDisabled
from .via_disk_folder import AppDataDiskFolder
from .via_tempdir import TempAppData


class AppDataAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        folder = self._check_folder(values)
        if folder is None:
            raise ArgumentError("app data path {} is not valid".format(values))
        setattr(namespace, self.dest, AppDataDiskFolder(folder))

    @staticmethod
    def _check_folder(folder):
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            try:
                os.makedirs(folder)
                logging.debug("created app data folder %s", folder)
            except OSError as exception:
                logging.info("could not create app data folder %s due to %r", folder, exception)
                return None
        return folder

    @staticmethod
    def default():
        key = str("VIRTUALENV_OVERRIDE_APP_DATA")
        if key in os.environ:
            candidate = os.environ[key]
        else:
            candidate = user_data_dir(appname="virtualenv", appauthor="pypa")

        folder = AppDataAction._check_folder(candidate)
        if folder is not None:
            return AppDataDiskFolder(folder)
        return AppDataDisabled()


__all__ = (
    "AppDataDiskFolder",
    "TempAppData",
    "AppDataAction",
    "AppDataDisabled",
)
