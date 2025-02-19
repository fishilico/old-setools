# Copyright 2014, Tresys Technology, LLC
#
# This file is part of SETools.
#
# SETools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SETools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SETools.  If not, see <http://www.gnu.org/licenses/>.
#
import unittest

import networkx as nx

from setools import SELinuxPolicy
from setools.infoflow import InfoFlowAnalysis
from setools.permmap import PermissionMap
from setools.policyrep.rule import RuleNotConditional


class InfoFlowAnalysisTest(unittest.TestCase):

    def setUp(self):
        self.p = SELinuxPolicy("tests/infoflow.conf")
        self.m = PermissionMap("tests/perm_map")

    def test_001_no_minimum(self):
        """Information flow analysis with no minimum weight."""

        a = InfoFlowAnalysis(self.p, self.m)
        a._build_graph()

        nodes = sorted(list(a.G.nodes_iter()))
        self.assertListEqual(["disconnected1", "disconnected2", "node1",
                              "node2", "node3", "node4", "node5",
                              "node6", "node7", "node8", "node9"], nodes)

        edges = sorted(list(a.G.out_edges_iter()))
        self.assertListEqual([("disconnected1", "disconnected2"),
                              ("disconnected2", "disconnected1"),
                              ("node1", "node2"),
                              ("node1", "node3"),
                              ("node2", "node4"),
                              ("node3", "node5"),
                              ("node4", "node6"),
                              ("node5", "node8"),
                              ("node6", "node5"),
                              ("node6", "node7"),
                              ("node8", "node9"),
                              ("node9", "node8")], edges)

        r = a.G.edge["disconnected1"]["disconnected2"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = a.G.edge["disconnected2"]["disconnected1"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node1"]["node2"]["rules"])
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node1")
        self.assertEqual(r[0].target, "node2")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["med_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        self.assertEqual(r[1].ruletype, "allow")
        self.assertEqual(r[1].source, "node2")
        self.assertEqual(r[1].target, "node1")
        self.assertEqual(r[1].tclass, "infoflow")
        self.assertSetEqual(set(["hi_r"]), r[1].perms)
        self.assertRaises(RuleNotConditional, getattr, r[1], "conditional")

        r = sorted(a.G.edge["node1"]["node3"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node3")
        self.assertEqual(r[0].target, "node1")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["low_r", "med_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node2"]["node4"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node2")
        self.assertEqual(r[0].target, "node4")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node3"]["node5"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node3")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["low_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node4"]["node6"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node4")
        self.assertEqual(r[0].target, "node6")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node5"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node8")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node6"]["node5"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node6")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["med_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node6"]["node7"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node6")
        self.assertEqual(r[0].target, "node7")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node8"]["node9"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node9"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

    def test_100_minimum_3(self):
        """Information flow analysis with minimum weight 3."""

        a = InfoFlowAnalysis(self.p, self.m, minweight=3)
        a._build_graph()

        nodes = sorted(list(a.G.nodes_iter()))
        self.assertListEqual(["disconnected1", "disconnected2", "node1",
                              "node2", "node3", "node4", "node5",
                              "node6", "node7", "node8", "node9"], nodes)

        edges = sorted(list(a.G.out_edges_iter()))
        self.assertListEqual([("disconnected1", "disconnected2"),
                              ("disconnected2", "disconnected1"),
                              ("node1", "node2"),
                              ("node1", "node3"),
                              ("node2", "node4"),
                              ("node4", "node6"),
                              ("node5", "node8"),
                              ("node6", "node5"),
                              ("node6", "node7"),
                              ("node8", "node9"),
                              ("node9", "node8")], edges)

        r = a.G.edge["disconnected1"]["disconnected2"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = a.G.edge["disconnected2"]["disconnected1"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node1"]["node2"]["rules"])
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node1")
        self.assertEqual(r[0].target, "node2")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["med_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        self.assertEqual(r[1].ruletype, "allow")
        self.assertEqual(r[1].source, "node2")
        self.assertEqual(r[1].target, "node1")
        self.assertEqual(r[1].tclass, "infoflow")
        self.assertSetEqual(set(["hi_r"]), r[1].perms)
        self.assertRaises(RuleNotConditional, getattr, r[1], "conditional")

        r = sorted(a.G.edge["node1"]["node3"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node3")
        self.assertEqual(r[0].target, "node1")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["low_r", "med_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node2"]["node4"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node2")
        self.assertEqual(r[0].target, "node4")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node4"]["node6"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node4")
        self.assertEqual(r[0].target, "node6")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node5"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node8")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node6"]["node5"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node6")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["med_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node6"]["node7"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node6")
        self.assertEqual(r[0].target, "node7")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node8"]["node9"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node9"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

    def test_200_minimum_8(self):
        """Information flow analysis with minimum weight 8."""

        a = InfoFlowAnalysis(self.p, self.m, minweight=8)
        a._build_graph()

        nodes = sorted(list(a.G.nodes_iter()))
        self.assertListEqual(["disconnected1", "disconnected2", "node1",
                              "node2", "node4", "node5",
                              "node6", "node7", "node8", "node9"], nodes)

        edges = sorted(list(a.G.out_edges_iter()))
        self.assertListEqual([("disconnected1", "disconnected2"),
                              ("disconnected2", "disconnected1"),
                              ("node1", "node2"),
                              ("node2", "node4"),
                              ("node4", "node6"),
                              ("node5", "node8"),
                              ("node6", "node7"),
                              ("node8", "node9"),
                              ("node9", "node8")], edges)

        r = a.G.edge["disconnected1"]["disconnected2"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = a.G.edge["disconnected2"]["disconnected1"]["rules"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "disconnected1")
        self.assertEqual(r[0].target, "disconnected2")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node1"]["node2"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node2")
        self.assertEqual(r[0].target, "node1")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_r"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node2"]["node4"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node2")
        self.assertEqual(r[0].target, "node4")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node4"]["node6"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node4")
        self.assertEqual(r[0].target, "node6")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node5"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node5")
        self.assertEqual(r[0].target, "node8")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node6"]["node7"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node6")
        self.assertEqual(r[0].target, "node7")
        self.assertEqual(r[0].tclass, "infoflow")
        self.assertSetEqual(set(["hi_w"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node8"]["node9"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")

        r = sorted(a.G.edge["node9"]["node8"]["rules"])
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].ruletype, "allow")
        self.assertEqual(r[0].source, "node8")
        self.assertEqual(r[0].target, "node9")
        self.assertEqual(r[0].tclass, "infoflow2")
        self.assertSetEqual(set(["super"]), r[0].perms)
        self.assertRaises(RuleNotConditional, getattr, r[0], "conditional")
