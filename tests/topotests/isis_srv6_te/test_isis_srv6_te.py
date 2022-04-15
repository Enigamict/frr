#!/usr/bin/env python


import os
import sys
import pytest
import json
from functools import partial

# Save the Current Working Directory to find configuration files.
CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CWD, "../"))

# pylint: disable=C0413
# Import topogen and topotest helpers
from lib import topotest
from lib.topogen import Topogen, TopoRouter, get_topogen
from lib.topolog import logger

# Required to instantiate the topology builder class.

pytestmark = [pytest.mark.bgpd, pytest.mark.isisd, pytest.mark.pathd]


def build_topo(tgen):
    "Build function"

    #
    # Define FRR Routers
    #
    for router in ["rt1", "rt2", "rt3", "rt4", "dst"]:
        tgen.add_router(router)

    #
    # Define connections
    #
    switch = tgen.add_switch("s1")
    switch.add_link(tgen.gears["rt1"], nodeif="eth-sw1")
    switch.add_link(tgen.gears["rt2"], nodeif="eth-sw1")

    switch = tgen.add_switch("s2")
    switch.add_link(tgen.gears["rt1"], nodeif="eth-sw2")
    switch.add_link(tgen.gears["rt3"], nodeif="eth-sw2")

    switch = tgen.add_switch("s3")
    switch.add_link(tgen.gears["rt2"], nodeif="eth-rt2")
    switch.add_link(tgen.gears["rt4"], nodeif="eth-rt4-1")

    switch = tgen.add_switch("s4")
    switch.add_link(tgen.gears["rt3"], nodeif="eth-rt3")
    switch.add_link(tgen.gears["rt4"], nodeif="eth-rt4-2")

    switch = tgen.add_switch("s9")
    switch.add_link(tgen.gears["rt4"], nodeif="eth-dst")
    switch.add_link(tgen.gears["dst"], nodeif="eth-rt4")


def setup_module(mod):
    "Sets up the pytest environment"

    tgen = Topogen(build_topo, mod.__name__)

    frrdir = tgen.config.get(tgen.CONFIG_SECTION, "frrdir")
    if not os.path.isfile(os.path.join(frrdir, "pathd")):
        pytest.skip("pathd daemon wasn't built")

    tgen.start_topology()

    router_list = tgen.routers()

    # For all registered routers, load the zebra configuration file
    for rname, router in router_list.items():
        router.load_config(
            TopoRouter.RD_ZEBRA, os.path.join(CWD, "{}/zebra.conf".format(rname))
        )
        router.load_config(
            TopoRouter.RD_ISIS, os.path.join(CWD, "{}/isisd.conf".format(rname))
        )
        router.load_config(
            TopoRouter.RD_PATH, os.path.join(CWD, "{}/pathd.conf".format(rname))
        )
        router.load_config(
            TopoRouter.RD_BGP, os.path.join(CWD, "{}/bgpd.conf".format(rname))
        )

    tgen.start_router()
    tgen.mininet_cli()


def teardown_module(mod):
    "Teardown the pytest environment"
    tgen = get_topogen()

    # This function tears down the whole topology.
    tgen.stop_topology()




# Memory leak test template
def test_memory_leak():
    "Run the memory leak test and report results."
    tgen = get_topogen()
    if not tgen.is_memleak_enabled():
        pytest.skip("Memory leak test/report is disabled")

    tgen.report_memory_leaks()


if __name__ == "__main__":
    args = ["-s"] + sys.argv[1:]
    sys.exit(pytest.main(args))
