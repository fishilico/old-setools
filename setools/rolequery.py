# Copyright 2014, Tresys Technology, LLC
#
# This file is part of SETools.
#
# SETools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2.1 of
# the License, or (at your option) any later version.
#
# SETools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SETools.  If not, see
# <http://www.gnu.org/licenses/>.
#
import re

from . import compquery


class RoleQuery(compquery.ComponentQuery):

    """Query SELinux policy roles."""

    def __init__(self, policy,
                 name="", name_regex=False,
                 types=set(), types_equal=False, types_regex=False):
        """
        Parameter:
        policy	     The policy to query.
        name         The role name to match.
        name_regex   If true, regular expression matching
                     will be used on the role names.
        types        The type to match.
        types_equal  If true, only roles with type sets
                     that are equal to the criteria will
                     match.  Otherwise, any intersection
                     will match.
        types_regex  If true, regular expression matching
                     will be used on the type names instead
                     of set logic.
        """

        self.policy = policy
        self.set_name(name, regex=name_regex)
        self.set_types(types, regex=types_regex, equal=types_equal)

    def results(self):
        """Generator which yields all matching roles."""

        for r in self.policy.roles():
            if r == "object_r":
                # all types are implicitly added to object_r by the compiler.
                # technically it is incorrect to skip it, but policy writers
                # and analysts don't expect to see it in results, and it
                # will confuse, especially for set equality type queries.
                continue

            if self.name and not self._match_regex(
                    r,
                    self.name,
                    self.name_regex,
                    self.name_cmp):
                continue

            if self.types and not self._match_regex_or_set(
                    set(str(t) for t in r.types()),
                    self.types,
                    self.types_equal,
                    self.types_regex,
                    self.types_cmp):
                continue

            yield r

    def set_types(self, types, **opts):
        """
        Set the criteria for the role's types.

        Parameter:
        types 		Name to match the role's types.

        Keyword Options:
        regex       If true, regular expression matching will be used
                    instead of set logic.
        equal		If true, the type set of the role
                    must equal the attributes criteria to
                    match. If false, any intersection in the
                    critera will cause a rule match.

        Exceptions:
        NameError   Invalid keyword option.
        """

        self.types = types

        for k in list(opts.keys()):
            if k == "regex":
                self.types_regex = opts[k]
            elif k == "equal":
                self.types_equal = opts[k]
            else:
                raise NameError("Invalid types option: {0}".format(k))

        if self.types_regex:
            self.types_cmp = re.compile(self.types)
        else:
            self.types_cmp = None
