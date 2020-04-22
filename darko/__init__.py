import logging.config
import os

## Sets the __version__ variable
from ._version import __version__
from .common import commons, get_git_revision_tag

# Remove old log file:
for filename in (f for f in os.listdir('.') if f.endswith('.darko.log')):
    try:
        os.remove(filename)
    except OSError:
        print ('Could not erase previous log file ' + filename)

# Logging: # TODO: Parametrize in darko cli or external config
_LOGCONFIG = {
     "version": 1,
     "disable_existing_loggers": False,
     'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)-8s] (%(funcName)s): %(message)s',
            'datefmt': '%y/%m/%d %H:%M:%S'
        },
        'notime': {
            'format': '[%(levelname)-8s] (%(funcName)s): %(message)s',
            'datefmt': '%y/%m/%d %H:%M:%S'
        },
     },
     "handlers": {
         "console": {
            "class": "darko.misc.colorstreamhandler.ColorStreamHandler",
             "stream": "ext://sys.stderr",
#             "stream": "sys.stdout",
             "level": "INFO",
             'formatter': 'notime',
         },

         "error_file": {
             "class": "logging.FileHandler",
             "level": "INFO",
             'formatter': 'standard',
             'filename': commons['logfile'],
             'encoding': 'utf8'

         }
     },

     "root": {
         "level": "INFO",
         "handlers": ["console", "error_file"],
     }
}


# Setting logging configuration:
try:
    logging.config.dictConfig(_LOGCONFIG)
except Exception:
    # if it didn't work, it might be due to ipython messing with the output
    # typical error: Unable to configure handler 'console': IOStream has no fileno
    # try without console output:
    print('WARNING: the colored console output is failing (possibly because of ipython). Switching to monochromatic '
          'output')
    _LOGCONFIG['handlers']['console']['class'] = "logging.StreamHandler"
    logging.config.dictConfig(_LOGCONFIG)

# Sets the __version__ variable
# try:
#     from setuptools_scm import get_version
#     import warnings
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         version = get_version(version_scheme='post-release',
#                               local_scheme=lambda version: version.format_choice("" if version.exact else "+{node}", "+dirty"), root='..', relative_to=__file__)
# except (ImportError, LookupError):
#     try:
#         from pkg_resources import get_distribution, DistributionNotFound
#         version = get_distribution(__package__).version
#     except DistributionNotFound:
#         logging.warning("Unable to detect version, most probably because you did not install it properly. "
#                         "To avoid further errors, please install it by running 'pip install -e .'.")
#         version = 'N/A'
__version__ = __version__ + str(get_git_revision_tag())


# Importing the main DARKO functions so that they can be called with "dk.function"
from .preprocessing.data_handler import load_config_excel
from .preprocessing.preprocessing import build_simulation

from .solve import solve_GAMS
#
#from .postprocessing.data_handler import get_sim_results, ds_to_df
#from .postprocessing.postprocessing import get_result_analysis, get_indicators_powerplant, aggregate_by_fuel, CostExPost
#from .postprocessing.plot import plot_energy_zone_fuel, plot_zone_capacities, plot_zone

from .cli import *


