#!/usr/bin/env python
"""
'**naming**' is a simple drop-in python library to solve and manage names by
setting configurable rules in the form of a naming convention.

[https://www.github.com/csaez/naming.git](https://www.github.com/csaez/naming.git)
"""

# The MIT License (MIT)
#
# Copyright (c) 2015 Cesar Saez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# == Helpers & Setup ==
import os
import json
import logging
from collections import OrderedDict

STR_TYPE = 0
DICT_TYPE = 1
INT_TYPE = 2

MEMO_DRIVER = 0
JSON_DRIVER = 1

FIELDS = dict()
PROFILES = dict()
ACTIVE_PROFILE = None


# == User Functions ==

def add_field(name, value, **kwds):
    """Add a `Field` to the naming convention."""
    field = Field(name, value, **kwds)
    FIELDS[name] = field
    return field


def add_profile(name, fields=None, active=False):
    """Add a new `Profile` to the naming convention."""
    profile = Profile(name)
    if fields:
        profile.add_field(fields)
    if active:
        set_active_profile(profile)
    PROFILES[name] = profile
    return profile


def set_active_profile(profile_name):
    """
    Set the active profile by name, all names will be solved under the rules set
    on this profile/context.
    """
    profile = PROFILES.get(profile_name)
    if profile:
        global ACTIVE_PROFILE  # patch ACTIVE_PROFILE, KISS
        ACTIVE_PROFILE = profile_name
        return True
    return False


def active_profile():
    """Get the active profile."""
    profile = PROFILES.get(ACTIVE_PROFILE)
    if ACTIVE_PROFILE and profile is not None:
        return profile
    return None


def save(driver=JSON_DRIVER):
    """
    Save all changes to disk in order to make them session persistent (only json
    is supported at the moment, if there's anyone wanting to add support to DB
    drivers please feels free to get in touch).
    """
    if driver == JSON_DRIVER:
        path = _path()
        if os.path.exists(path):
            os.mkdir(path)

    if driver == MEMO_DRIVER:  # in memory, used by unit tests
        pass


def _path():
    """
    Return the path where naming gets serialized (kinda coupled with `save()`
    and `JSON_DRIVER` at the moment, KISS).

    The mechanism follows the order below:

    1. Look at `NAMING_PATH` environment variable.
    2. Look at `~/.local/share/naming.py/`

    > `~` is equvalent to `%userprofile%` on Windows... yay! :)
    """
    home = os.path.expanduser("~")
    return os.environ.get("NAMING_PATH",
                          os.path.join(home, ".local", "share", "naming.py"))


# == Classes ==

class Field(object):
    """This object represent one of the fields/tokens composing the name.

    A name is generally composed by multiple fields, so in order to
    solve/unsolve the final name the library go through each field looking at
    possible answers and pick the best combination possible depending on the
    active `Profile`, allowing the user to skip field values by getting them
    implicitly.

    Fields can be of 3 types (implicitly determined by its value type):

    - `STR_TYPE`: a text field (str/unicode).
    - `DICT_TYPE`: a mapping table (dict).
    - `INT_TYPE`: an integer number (int).
    """

    def __init__(self, name, value, **kwds):
        super(Field, self).__init__()

        self.name = name
        self.value = value

        {str: self._initStr,
         dict: self._initDict,
         int: self._initInt}.get(type(self.value))(**kwds)

        self.required = True if self.default is None else False

    def _initStr(self, **kwds):
        self._type = STR_TYPE
        self.default = kwds.get("default")

    def _initDict(self, **kwds):
        self._type = DICT_TYPE
        self.default = kwds.get("default", self.value.values()[0])

    def _initInt(self, **kwds):
        self._type = INT_TYPE
        self.default = kwds.get("default", 0)
        self.padding = kwds.get("padding", 3)

    def solve(self, *values):
        """Solve the field by returning a `set` of possible answers."""
        rval = set()  # set of possible values

        for val in values:
            if self._type == STR_TYPE:
                if not isinstance(val, basestring) and self.required:
                    rval.add(val)
            if self._type == DICT_TYPE:
                v = self.value.get(val)
                if v is not None:
                    rval.add(v)
            if self._type == INT_TYPE:
                if type(val) == int:
                    v = str(val).zfill(self.padding)
                    rval.add(v)
            else:
                logging.error("Invalid type: {}".format(val))

        if not len(rval) and self.default:
            rval.add(self.default)

        return rval

    def unsolve(self, *values):
        """Decode a name returning the corresponding mapping."""
        pass


class Profile(object):
    """This object represents a name Profile.

    A Profile groups a set of fields (each one with their own rules) allowing to
    solve/unsolve whole names in different contexts (saving a file to disk,
    naming an instance in a dependency graph and so on).
    """
    def __init__(self, name, fields=None):
        super(Profile, self).__init__()
        self.name = name
        self.fields = OrderedDict()  # order is important!
        self.separator = "_"

        if fields is not None:
            self.add_fields(fields)

    def add_field(self, field):
        """Add a field to this profile."""
        if not isinstance(field, Field):
            logging.error("{} is not a Field".format(field))
            return False
        self.fields[field.name] = field
        return True

    def add_fields(self, fields):
        """Add fields (`iterable`) to this profile."""
        for f in fields:
            self.add_field(f)

    def solve(self, *values):
        """Solve a name based on user input and profile fields."""
        rval = list()
        for name, field in self.fields.iteritems():
            rval.append(name, field.solve(*values))
        return rval

    def unsolve(self, name):
        """Return a `dict` mapping field key values."""
        rval = list()
        values = name.split(self.separator)
        for name, field in self.fields.iteritems():
            rval.append(name, field.unsolve(*values))
        return rval
