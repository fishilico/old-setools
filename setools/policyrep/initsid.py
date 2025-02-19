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
from . import qpol
from . import symbol
from . import context


class InitialSID(symbol.PolicySymbol):

    """An initial SID statement."""

    @property
    def context(self):
        """The context for this initial SID."""
        return context.Context(self.policy, self.qpol_symbol.context(self.policy))

    def statement(self):
        return "sid {0} {1}".format(self, self.context)
