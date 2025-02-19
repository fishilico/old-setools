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


class PermissiveQuery(compquery.ComponentQuery):

    """Query permissive types"""

    def __init__(self, policy,
                 name="", name_regex=False):
        """
        Parameters:
        name        The name of the policy capability to match.
        name_regex  If true, regular expression matching will
                    be used for matching the name.
        """

        self.policy = policy
        self.set_name(name, regex=name_regex)

    def results(self):
        """Generator which yields all matching permissive types."""

        for t in self.policy.permissives():
            if self.name and not self._match_regex(
                    t,
                    self.name,
                    self.name_regex,
                    self.name_cmp):
                continue

            yield t
