#
# @Author : Jean-Pascal Mercier <jean-pascal.mercier@agsis.com>
#
# @Copyright (C) 2010 Jean-Pascal Mercier
#
# All rights reserved.
#
#

__doc__ = """
"""

from SCons.Script import Builder

import cPickle as pickle
import numpy as np
from agstd.tools import np_load

def PerturbateColumnAction(source, target, env):
    """
    Source :    0 - Input file
                1 - Column Name
                3 - Optional/
    """
    infile = str(source[0])
    colname, stdev = [s.value for s in source[1:3]]

    outfile = str(target[0])
    inobj = np_load(infile)

    intable = inobj[source[3].value] if len(source) > 3 else inobj

    intable[colname] += np.random.normal(scale = stdev, size = len(intable[colname]))

    if inobj != intable:
        inobj[source[3].value] = intable

    pickle.dump(inobj, open(outfile, 'wb'), protocol = pickle.HIGHEST_PROTOCOL)



def generate(env):
    env['BUILDERS']['PerturbateColumn'] = \
            Builder(action = PerturbateColumnAction)

def exists(env):
    return 1
