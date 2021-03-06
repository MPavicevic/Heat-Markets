# -*- coding: utf-8 -*-
"""
This worksheet contains the two main functions to solve the DARKO optimization problem using  GAMS.

Solve with GAMS and the high level API
--------------------------------------
The high level interface is recommended for Linux users because it solves
the "whitespace in the simulation folder" issue.

Installation:
    To install the high-level API in Python 2.x::

        cd gams24.4_linux_x64_64_sfx/apifiles/Python/api
        python gamssetup.py install

    To install the high-level API in Python 3.x::
    
        cd gams24.6_linux_x64_64_sfx/apifiles/Python/api_34
        python setup.py install    

Solve with GAMS and the low level APIs
--------------------------------------
Use lower level apis to run GAMS. BAsed on GAMS xpexample2.py

The advantage of the low level API is that it can easily be installed from pip::
    
    pip install gdxcc
    pip install gamsxcc
    pip install optcc
"""

#######################################################################################################################
############################################## DARKO: main model ######################################################
#######################################################################################################################


import os
import shutil
import logging

from .misc.gdx_handler import get_gams_path, import_local_lib, package_exists
from .misc.gms_handler import solve_high_level, solve_low_level
from .common import commons, set_log_name


def is_sim_folder_ok(sim_folder):
    """
    Function that checks if the provided path is a valid DARKO simulation folder.
    The following files are required:

        - Inputs.gdx
        - DARKO.gms

    :param sim_folder: path (absolute or relative) to the simulation folder
    """
    if not os.path.exists(sim_folder):
        logging.error('The provided DARKO simulation environment folder (' + sim_folder + ') does not exist')
        return False

    str1 = 'There is no '
    str2 = ' file within the specified DARKO simulation environment folder (' + sim_folder + ').'
    str3 = ' Check that the GDX output is activated in the option file and no error is stated during the pre-processing'

    if not os.path.exists(os.path.join(sim_folder, u'Inputs.gdx')):
        logging.error(str1 + 'Inputs.gdx' + str2 + str3)
        return False
    if not os.path.exists(os.path.join(sim_folder, u'DARKO.gms')):
        logging.error(str1 + 'DARKO.gms' + str2)
        return False
    return True


def solve_GAMS(sim_folder, gams_folder=None, gams_file='DARKO.gms', result_file='Results.gdx', output_lst=False):
    """
    Function used to run the optimization using the GAMS engine.

    :param sim_folder:      path to a valid DARKO simulation folder
    :param gams_folder:     path to the gams folder. If not provided, the script will try to find it automatically
    :param gams_file:       GAMS file to be called for the optimization
    :param result_file:     Name of the results file
    :param output_lst:      Set to True to conserve a copy of the GAMS lst file in the simulation folder
    """

    if package_exists('gamsxcc') and package_exists('optcc'):
        solv_func = solve_low_level
        logging.info('Using the low-level gams api')
    elif package_exists('gams'):
        solv_func = solve_high_level
        logging.info('Using the high-level gams api')
    else:
        logging.warning('Could not find the GAMS APIs. Trying to locate local version')
        if not import_local_lib('lowlevel'):
            return False
    gams_folder = get_gams_path(gams_folder)
    if not gams_folder:  # couldn't locate
        logging.error('GAMS path cannot be located. Simulation is stopped')
        return False
    sim_folder = os.path.abspath(sim_folder)
    gams_folder = os.path.abspath(gams_folder)

    if is_sim_folder_ok(sim_folder):
        # Temporary warning for Spyder users:
        if any(['SPY_' in name for name in os.environ]):  # check if spyder
            logging.info(
                "\nIf the script seems stuck at this place \n(gams is optimizing but not output is displayed), "
                "\nit is preferable to run DARKO in a \nseparate terminal (in Spyder: Preferences - Run - \nExecute "
                "in an external system terminal)")
        ret = solv_func(gams_folder, sim_folder, gams_file, result_file, output_lst=output_lst)
        if os.path.isfile(os.path.join(sim_folder, 'debug.gdx')):
            logging.warning('A debug file was created. There has probably been an optimization error')
        set_log_name(sim_folder, 'warn_solve')
        return ret
    else:
        return False
