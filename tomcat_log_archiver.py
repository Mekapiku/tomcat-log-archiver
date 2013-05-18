#!/usr/bin/env python
#coding: UTF-8

#############################
#          Imports          #
#############################
import os
import re
import logging
import shutil
import tempfile

import distutils.archive_util

##############################
#           Class            #
##############################
class LogArchiver(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def archive(self, regex, get_archive_name, archive_type="zip", delete_flag=False):
         # params type check
        if not type(regex) is type(re.compile("")):
            logging.info("Argument is bad. Please input re.complie pattern.")
            return None

        # if not exist or not access directory
        if not (os.path.exists(self.dir_path) and os.access(self.dir_path, os.R_OK)):
            logging.warning("Directory is Permission denied.")
            return None

        # archive type decide
        if archive_type == "zip":
            archive_type = "zip"
        elif archive_type == "gzip":
            archive_type = "gzip"
        elif archive_type == "bzip2":
            archive_type = "tar.bz2"
        else:
            archive_type = "zip"

        archive_list = []

        # pickup log files by dir
        for file in os.listdir(self.dir_path):
            if regex.search(file) is not None:
                archive_list.append(self.dir_path + "/" + file)

        # if archive_list is null, return None
        if len(archive_list) < 1:
            logging.info("Noting is to archive logs.")
            return None

        # check exists directory
        archive_name = os.path.normpath(get_archive_name(archive_list))
        if os.path.exists(archive_name):
            logging.warning("already exists directory: %(archive_name)s" % locals())
            return None
        # if string end is "/", delete it.
        while archive_name.endswith("/"):
            archive_name.rstrip("/")

        archive_dir = os.path.dirname(archive_name)
        archive_name = os.path.abspath(archive_name)
        logging.debug("archive_name: " + archive_name)
        logging.debug("archive_dir: " + archive_dir)

        # check exists file
        logging.debug("archive name: " + os.path.join(archive_dir, archive_name + "." + archive_type))

        if os.path.exists(os.path.join(archive_dir, archive_name + "." + archive_type)):
            logging.warning("Already exists file: %(archive_name)s.%(archive_type)s" % locals())
            return None

        if not os.path.exists(archive_dir):
            # make directory
            try:
                os.makedirs(archive_dir)
            except OSError, msg:
                logging.warning(msg)
                logging.warning("arhive direcoty can not make")
                return None

            # check directory permission
            if not os.access(archive_dir, os.W_OK):
                os.chmod(archive_dir, os.stat.S_IWUSR)

        # make temp dir
        tmp_dir = tempfile.mkdtemp(dir=archive_dir)

        for file in archive_list:
            if delete_flag:
                shutil.move(file, tmp_dir)
            else:
                shutil.copy(file, tmp_dir)

        # compression directory
        if archive_type == "zip":
            distutils.archive_util.make_zipfile(archive_name, tmp_dir)
        elif archive_type == "gzip":
            distutils.archive_util.make_tarball(archive_name, tmp_dir, compress='gzip')
        elif archive_type == "tar.bz2":
            distutils.archive_util.make_tarball(archive_name, tmp_dir, compress='bzip2')
        else:
            distutils.archive_util.make_zipfile(archive_name, tmp_dir)

        logging.debug("archive_type: " + archive_type)

        # delete temp dir
        shutil.rmtree(tmp_dir)

        # end
        logging.info("Logs Archive is Success.")


    def set_path(self, dir_path):
        self.dir_path = dir_path



