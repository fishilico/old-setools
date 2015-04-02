# Copyright 2014-2015, Tresys Technology, LLC
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


class PolicyQuery(object):

    """Abstract base class for SELinux policy queries."""

    @staticmethod
    def _match_regex(obj, criteria, regex):
        """
        Match the object with optional regular expression.

        Parameters:
        obj         The object to match.
        criteria    The criteria to match.
        regex       If regular expression matching should be used.
        """

        if regex:
            return bool(criteria.search(str(obj)))
        else:
            return (obj == criteria)

    @staticmethod
    def _match_set(obj, criteria, equal):
        """
        Match the object (a set) with optional set equality.

        Parameters:
        obj         The object to match. (a set)
        criteria    The criteria to match. (a set)
        equal       If set equality should be used. Otherwise
                    any set intersection will match.
        """

        if equal:
            return (obj == criteria)
        else:
            return bool(obj.intersection(criteria))

    @staticmethod
    def _match_in_set(obj, criteria, regex):
        """
        Match if the criteria is in the list, with optional
        regular expression matching.

        Parameters:
        obj         The object to match.
        criteria    The criteria to match.
        regex       If regular expression matching should be used.
        """

        if regex:
            return bool(list(filter(criteria.search, (str(m) for m in obj))))
        else:
            return (criteria in obj)

    @staticmethod
    def _match_regex_or_set(obj, criteria, equal, regex):
        """
        Match the object (a set) with either set comparisons
        (equality or intersection) or by regex matching of the
        set members.  Regular expression matching will override
        the set equality option.

        Parameters:
        obj         The object to match. (a set)
        criteria    The criteria to match.
        equal       If set equality should be used.  Otherwise
                    any set intersection will match. Ignored
                    if regular expression matching is used.
        regex       If regular expression matching should be used.
        """

        if regex:
            return bool(list(filter(criteria.search, (str(m) for m in obj))))
        else:
            return PolicyQuery._match_set(obj, set(criteria), equal)

    @staticmethod
    def _match_range(obj, criteria, subset, overlap, superset, proper):
        """
        Match ranges of objects.

        obj         A 2-tuple of the range to match.
        criteria    A 2-tuple of the criteria to match.
        subset      If true, the criteria will match if it is a subset obj's range.
        overlap     If true, the criteria will match if it overlaps any of the obj's range.
        superset    If true, the criteria will match if it is a superset of the obj's range.
        proper      If true, use proper superset/subset operations.
                    No effect if not using set operations.
        """
        # use nicer names to make the below conditions easier to read.
        obj_low = obj[0]
        obj_high = obj[1]
        crit_low = criteria[0]
        crit_high = criteria[1]

        if overlap:
            return ((obj_low <= crit_low <= obj_high) or (
                     obj_low <= crit_high <= obj_high) or (
                     crit_low <= obj_low and obj_high <= crit_high))
        elif subset:
            if proper:
                return ((obj_low < crit_low and crit_high <= obj_high) or (
                         obj_low <= crit_low and crit_high < obj_high))
            else:
                return (obj_low <= crit_low and crit_high <= obj_high)
        elif superset:
            if proper:
                return ((crit_low < obj_low and obj_high <= crit_high) or (
                         crit_low <= obj_low and obj_high < crit_high))
            else:
                return (crit_low <= obj_low and obj_high <= crit_high)
        else:
            return (crit_low == obj_low and obj_high == crit_high)

    @staticmethod
    def _match_level(obj, criteria, dom, domby, incomp):
        """
        Match the an MLS level.

        obj         The level to match.
        criteria    The criteria to match. (a level)
        dom         If true, the criteria will match if it dominates obj.
        domby       If true, the criteria will match if it is dominated by obj.
        incomp      If true, the criteria will match if it is incomparable to obj.
        """

        if dom:
            return (criteria >= obj)
        elif domby:
            return (criteria <= obj)
        elif incomp:
            return (criteria ^ obj)
        else:
            return (criteria == obj)

    def results(self):
        """
        Generator which returns the matches for the query.  This method
        should be overridden by subclasses.
        """
        raise NotImplementedError
