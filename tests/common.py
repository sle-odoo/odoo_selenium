# -*- coding: utf-8 -*-

from hashlib import md5
from selenium import webdriver
from shutil import rmtree
from socket import socket
from sys import platform
from unittest import SkipTest, TestCase
from uuid import uuid4

import os
import subprocess
import tarfile


# -----------------------------------------------------------------------------
# Postgres and Odoo helpers
# -----------------------------------------------------------------------------
ODOO_DIR = os.getenv('ODOO_DIR')
DBDUMP_DIR = os.getenv('DBDUMP_DIR')
ENTERPRISE_DIR = os.getenv('ENTERPRISE_DIR')
if ENTERPRISE_DIR is None:
    ENTERPRISE_DIR = os.path.join(ODOO_DIR, '..', 'enterprise')
if platform == 'darwin':
    FILESTORE_ROOT = os.path.expanduser("~/Library/Application Support/Odoo/filestore")
else:  # sys.platform == 'linux'
    FILESTORE_ROOT = os.path.expanduser("~/.local/share/Odoo/filestore")


def db_create(name, dependencies):
    cmd = [
        './odoo-bin',
        '--addons-path', '../enterprise,./addons',
        '-d', '%s' % name,
        '-i', '%s' % ','.join(dependencies),
        '--without-demo', 'all',
        '--stop-after-init'
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ODOO_DIR)
    out, err = process.communicate()
    if process.returncode:
        raise ValueError(err)

    deps = ' ,'.join(dependencies)
    rev1, rev2 = odoo_git_revision()
    print "created a new database (dependencies: %s, odoo rev: %s, enteprise rev: %s" % (deps, rev1, rev2)


def db_drop(name):
    cmd = 'dropdb %s' % name
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode:
        raise ValueError(err)
    rmtree(os.path.join(FILESTORE_ROOT, name))
    print "dropped database %s" % name


def dbdump_exist(name):
    if os.path.isfile(os.path.join(DBDUMP_DIR, '%s.sql' % name)):
        print "found dump %s" % name
        return True
    print "not found dump %s" % name
    return False


def dbdump_create(name):
    cmd = 'pg_dump %s > %s' % (name, os.path.join(DBDUMP_DIR, '%s.sql' % name))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode:
        raise ValueError(err)
    filestore_src_path = os.path.join(FILESTORE_ROOT, name)
    filestore_dst_path = os.path.join(DBDUMP_DIR, '%s.tar' % name)
    tar = tarfile.open(filestore_dst_path, 'w')
    for _dir in os.listdir(filestore_src_path):
        tar.add(os.path.join(filestore_src_path, _dir), arcname=_dir)
    tar.close()
    print "created dump %s" % name


def dbdump_restore(dumpname, dbname):
    cmd = 'createdb %s && psql %s < %s' % (dbname, dbname, os.path.join(DBDUMP_DIR, '%s.sql' % dumpname))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode:
        raise ValueError(err)
    filestore_dump = os.path.join(DBDUMP_DIR, '%s.tar' % dumpname)
    new_fs = os.path.join(FILESTORE_ROOT, dbname)
    os.mkdir(new_fs)
    tarfile.open(filestore_dump, 'r').extractall(new_fs)
    print "restored dump %s into database %s" % (dumpname, dbname)


def odoo_spawn(name):
    def _get_free_port():
        s = socket()
        s.bind(('', 0))
        return s.getsockname()[1]

    port = _get_free_port()
    cmd = [
        './odoo-bin',
        '--addons-path', '%s,./addons' % ENTERPRISE_DIR,
        '-d', '%s' % name,
        '--db-filter', '^%s$' % name,
        '--xmlrpc-port', str(port),
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ODOO_DIR)
    print "spawned an odoo instance at port %s" % port
    return process, 'http://localhost:%s' % port


def odoo_git_revision():
    cmd = 'git rev-parse HEAD'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=ODOO_DIR)
    rev_odoo = process.communicate()[0]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=ENTERPRISE_DIR)
    rev_enterprise = process.communicate()[0]
    return [rev_odoo, rev_enterprise]


# -----------------------------------------------------------------------------
# Testcases implementation
# -----------------------------------------------------------------------------
class SeleniumCase(TestCase):

    _depends = []  # Odoo modules the test depends on

    @property
    def hash(self):
        """
        Used in order to identify a database that will honour the dependencies
        and the git state of the Odoo repositories.

        :return: hash of the testcase, will be used to create a database valid for this test
        """
        hash_input = ','.join(odoo_git_revision() + self._depends)
        hash_object = md5(hash_input)
        return hash_object.hexdigest()

    def setUp(self):
        super(SeleniumCase, self).setUp()

        # setup the database
        self.dbname = '%s_%s' % (self.hash, str(uuid4()))
        self.dbname = self.dbname[:63]
        if not dbdump_exist(self.hash):
            try:
                db_create(self.hash, self._depends)
                dbdump_create(self.hash)
                db_drop(self.hash)  # this database was only used to create a dump
            except ValueError, e:
                print '%r: unable to setup the database, skipping\n%s' % (self, e.message)
                raise SkipTest()
        dbdump_restore(self.hash, self.dbname)

        self.odoo_process, self.odoo_url = odoo_spawn(self.dbname)
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()
        self.odoo_process.kill()
        db_drop(self.dbname)
        super(SeleniumCase, self).tearDown()

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc and ' '.join(filter(None, map(str.strip, doc.splitlines()))) or None
