"""
Parse and modify BEAST/MASTER NEXUS tree outputs by transferring the contents of the
comment strings to the node labels.  The purpose of this is to make these outputs
more readable by BioPython.

Terminal node label has the format:
1[&type="I",location="0",reaction="Sampling",time=0.2458663625884157]:0.12195191891543124
Internal node label has the format:
...)[&type="I",location="0",reaction="Infection",time=0.15089530647673044]:0.011186556452893681
"""
import re
import sys

from glob import glob


def get_transmissions(fn):
    """
    Complete edge list
    """
    pass
