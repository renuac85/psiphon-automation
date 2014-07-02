#!/usr/bin/python
#
# Copyright (c) 2011, Psiphon Inc.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import shlex
import subprocess
import psi_ops_stats_credentials
import logging

PSI_OPS_DB_FILENAME = os.path.join(os.path.abspath('.'), 'psi_ops_stats.dat')
# Can't overwrite target file directly due to Wine limitation
export_filename = os.path.join(os.path.abspath('.'), 'psi_ops_stats.dat.temp')

if __name__ == "__main__":
    try:
        logging.basicConfig(filename='psi_update_stats_dat.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
        if os.path.isfile(export_filename):
            logging.info('Removing temp file')
            os.remove(export_filename)
        cmd = 'wine ./CipherShare/CipherShareScriptingClient.exe \
                ExportDocument \
                -UserName %s -Password %s \
                -OfficeName %s -DatabasePath "%s" -ServerHost %s -ServerPort %s \
                -SourceDocument "%s" \
                -TargetFile "%s"' \
             % (psi_ops_stats_credentials.CIPHERSHARE_USERNAME,
                psi_ops_stats_credentials.CIPHERSHARE_PASSWORD,
                psi_ops_stats_credentials.CIPHERSHARE_OFFICENAME,
                psi_ops_stats_credentials.CIPHERSHARE_DATABASEPATH,
                psi_ops_stats_credentials.CIPHERSHARE_SERVERHOST,
                psi_ops_stats_credentials.CIPHERSHARE_SERVERPORT,
                psi_ops_stats_credentials.CIPHERSHARE_PSI_OPS_STATS_DOCUMENT_PATH,
                export_filename)

        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.communicate()

        if proc.returncode != 0:
            msg = 'CipherShare export failed %s' % str(output)
            logging.warning(msg)
            raise Exception(msg)

        if os.path.isfile(export_filename):
            if os.path.isfile(PSI_OPS_DB_FILENAME):
                os.remove(PSI_OPS_DB_FILENAME)
                logging.info('%s removed', PSI_OPS_DB_FILENAME)
            os.rename(export_filename, PSI_OPS_DB_FILENAME)
            logging.info('%s renamed to %s', export_filename, PSI_OPS_DB_FILENAME)
        else:
            logging.info('%s is not found', export_filename)

    except Exception as e:
        logging.warning('Exception: %s', str(e)) 
        print str(e)
