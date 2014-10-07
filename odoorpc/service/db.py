# -*- coding: UTF-8 -*-
##############################################################################
#
#    OdooRPC
#    Copyright (C) 2014 Sébastien Alix.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""Provide the :class:`DB` class in order to manage the server databases."""
import base64
import io

from odoorpc import error


class DB(object):
    """The `DB` class represents the database management service.
    It provides functionalities such as list, create, drop, dump
    and restore databases.

    .. note::
        This service have to be used through the :attr:`odoorpc.ODOO.db`
        property.

    >>> import odoorpc
    >>> odoo = odoorpc.ODOO('localhost')
    >>> odoo.db
    <odoorpc.service.db.DB object at 0x7f95b76fdbd0>

    """
    def __init__(self, odoo):
        self._odoo = odoo

    def dump(self, password, db):
        """Backup the `db` database. Returns the dump as a binary ZIP file
        containing the SQL dump file alongside the filestore directory (if any).

        >>> dump = odoo.db.backup('super_admin_passwd', 'prod')

        If you get a timeout error, increase this one before performing the
        request:

        >>> timeout_backup = odoo.config['timeout']
        >>> odoo.config['timeout'] = 600    # Timeout set to 10 minutes
        >>> dump = odoo.db.backup('super_admin_passwd', 'prod')
        >>> odoo.config['timeout'] = timeout_backup

        Write it on the file system:

        >>> with open('dump.zip', 'w') as dump_zip:
        ...     dump_zip.write(dump.read())
        ...

        You can manipulate the file with the `zipfile` module for instance:

        >>> import zipfile
        >>> zipfile.ZipFile('dump.zip').namelist()
        ['dump.sql',
         'filestore/ef/ef2c882a36dbe90fc1e7e28d816ad1ac1464cfbb',
         'filestore/dc/dcf00aacce882bbfd117c0277e514f829b4c5bf0']

        The super administrator password is required to perform this method.

        *Python 2:*

        :return: `io.BytesIO`
        :raise: :class:`odoorpc.error.RPCError` (access denied / wrong database)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: `io.BytesIO`
        :raise: :class:`odoorpc.error.RPCError` (access denied / wrong database)
        :raise: `urllib.error.URLError` (connection error)
        """
        data = self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'dump',
             'args': [password, db]})
        binary_data = base64.standard_b64decode(data['result'])
        return io.BytesIO(binary_data)

    def change_password(self, password, new_password):
        """Change the administrator password by `new_password`.

        >>> odoo.db.change_password('super_admin_passwd', 'new_admin_passwd')

        The super administrator password is required to perform this method.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'change_admin_password',
             'args': [password, new_password]})

    def create(self, password, db, demo=False, lang='en_US', admin_password='admin'):
        """Request the server to create a new database named `db`
        which will have `admin_password` as administrator password and
        localized with the `lang` parameter.
        You have to set the flag `demo` to `True` in order to insert
        demonstration data.

        >>> odoo.db.create('super_admin_passwd', 'prod', False, 'fr_FR', 'my_admin_passwd')

        If you get a timeout error, increase this one before performing the
        request:

        >>> timeout_backup = odoo.config['timeout']
        >>> odoo.config['timeout'] = 600    # Timeout set to 10 minutes
        >>> odoo.db.create('super_admin_passwd', 'prod', False, 'fr_FR', 'my_admin_passwd')
        >>> odoo.config['timeout'] = timeout_backup

        The super administrator password is required to perform this method.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'create_database',
             'args': [password, db, demo, lang, admin_password]})

    def drop(self, password, db):
        """Drop the `db` database. Returns `True` if the database was removed,
        `False` otherwise (database did not exist):

        >>> odoo.db.drop('super_admin_passwd', 'test')
        True

        The super administrator password is required to perform this method.

        *Python 2:*

        :return: `True` or `False`
        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: `True` or `False`
        :raise: :class:`odoorpc.error.RPCError` (access denied)
        :raise: `urllib.error.URLError` (connection error)
        """
        data = self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'drop',
             'args': [password, db]})
        return data['result']

    def duplicate(self, password, db, new_db):
        """Duplicate `db' as `new_db`.

        >>> odoo.db.duplicate('super_admin_passwd', 'prod', 'test')

        The super administrator password is required to perform this method.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError` (access denied / wrong database)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError` (access denied / wrong database)
        :raise: `urllib.error.URLError` (connection error)
        """
        self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'duplicate_database',
             'args': [password, db, new_db]})

    def list(self):
        """Return the list of the databases:

        >>> odoo.db.list()
        ['prod', 'test']

        *Python 2:*

        :return: `list` of database names
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :return: `list` of database names
        :raise: `urllib.error.URLError` (connection error)
        """
        data = self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'list',
             'args': []})
        return data.get('result', [])

    def restore(self, password, db, dump, copy=False):
        """Restore the `dump` database into the new `db` database.
        The `dump` file object can be obtained with the
        :func:`dump <DB.dump>` method.
        If `copy` is set to `True`, the restored database will have a new UUID.

        >>> odoo.db.restore('super_admin_passwd', 'test', dump_file)

        If you get a timeout error, increase this one before performing the
        request:

        >>> timeout_backup = odoo.config['timeout']
        >>> odoo.config['timeout'] = 7200   # Timeout set to 2 hours
        >>> odoo.db.restore('super_admin_passwd', 'test', dump_file)
        >>> odoo.config['timeout'] = timeout_backup

        The super administrator password is required to perform this method.

        *Python 2:*

        :raise: :class:`odoorpc.error.RPCError`
                (access denied / database already exists)
        :raise: :class:`odoorpc.error.InternalError` (dump file closed)
        :raise: `urllib2.URLError` (connection error)

        *Python 3:*

        :raise: :class:`odoorpc.error.RPCError`
                (access denied / database already exists)
        :raise: :class:`odoorpc.error.InternalError` (dump file closed)
        :raise: `urllib.error.URLError` (connection error)
        """
        if dump.closed:
            raise error.InternalError("Dump file closed")
        b64_data = base64.standard_b64encode(dump.read()).decode()
        self._odoo.json(
            '/jsonrpc',
            {'service': 'db',
             'method': 'restore',
             'args': [password, db, b64_data, copy]})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
