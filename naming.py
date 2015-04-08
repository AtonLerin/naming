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

PROFILES = {"current": ""}


class Profile(object):

    def __init__(self, name):
        self.name = name
        self.fields = list()

        self.separator = "_"
        self.tokens = dict()

    def add_field(self, name):
        f = Field(name)
        self.fields.append(f)
        return f

    def list_fields(self):
        return [f.name for f in self.fields]

    def solve(self, *arg, **kwds):
        non_default = list()
        for f in self.fields:
            if f.has_default:
                f.value = f.default
            else:
                non_default.append(f)
        if len(non_default) != len(arg):
            return None
        for a in list(arg):
            for f in self.fields:
                if a in f.tokens:
                    f.solve(a)
                    arg.remove(a)
        for k, v in kwds.iteritems():
            f = self.get_field(k)
            f.solve(v)
        i = 0
        for f in self.fields:
            if not f.value:
                f.value = arg[i]
                i += 1
        return self.separator.join([x.value for x in self.fields])


class Field(object):

    def __init__(self, name):
        self.name = name
        self.value = ""
        self.tokens = list()
        self.default = None
        self.has_default = False

    def append_token(self, token, default=False):
        self.tokens.append(token)
        if default:
            self.set_default(token)

    def set_default(self, value):
        self.has_default = True
        self.default = get_token(value)

    def solve(self, token):
        self.value = token


def solve(*arg, **kwds):
    p = current_profile()
    return p.solve(*arg, **kwds)


def list_tokens():
    p = current_profile()
    return p.tokens.keys()


def get_token(key):
    p = current_profile()
    return p.tokens.get(key)


def new_token(name, value):
    if not get_token(name):
        p = current_profile()
        p.tokens[name] = value
        return True
    return False


def delete_token(name):
    if get_token(name):
        p = current_profile()
        del p.tokens[name]
        return True
    return False


def clear_tokens():
    p = current_profile()
    p.tokens.clear()


def list_profiles():
    return [x for x in PROFILES.keys() if x != "current"]


def new_profile(name):
    if PROFILES.get(name):
        return None
    PROFILES[name] = Profile(name)
    set_profile(name)
    return PROFILES[name]


def get_profile(name):
    p = PROFILES.get(name)
    if p and name == "current":
        return PROFILES.get(p)
    return p


def set_profile(name):
    if PROFILES.get(name):
        PROFILES["current"] = name
        return True
    return False


def current_profile():
    name = PROFILES["current"]
    p = PROFILES.get(name)
    if p:
        return p
    PROFILES["current"] = ""
    return None


def delete_profile(name):
    if name == "current":
        name = PROFILES[name]
    if PROFILES.get(name):
        del PROFILES[name]
        ps = list_profiles()
        if len(ps):
            set_profile(ps[0])
        else:
            PROFILES["current"] = ""
