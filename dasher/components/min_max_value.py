# Copyright (c) 2015 Project Jupyter Contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from numbers import Real


def get_min_max_value(min, max, x=None, step=None):
    """Return min, max, x given input values with possible None."""
    # Either min and max need to be given, or x needs to be given
    if x is None:
        if min is None or max is None:
            raise ValueError(
                "unable to infer range, x from: ({0}, {1}, {2})".format(
                    min, max, x
                )
            )
        diff = max - min
        x = min + (diff / 2)
        # Ensure that x has the same type as diff
        if not isinstance(x, type(diff)):
            x = min + (diff // 2)
    else:  # x is not None
        if not isinstance(x, Real):
            raise TypeError("expected a real number, got: %r" % x)
        # Infer min/max from x
        if x == 0:
            # This gives (0, 1) of the correct type
            vrange = (x, x + 1)
        elif x > 0:
            vrange = (-x, 3 * x)
        else:
            vrange = (3 * x, -x)
        if min is None:
            min = vrange[0]
        if max is None:
            max = vrange[1]
    if step is not None:
        # ensure x is on a step
        tick = int((x - min) / step)
        x = min + tick * step
    if not min <= x <= max:
        raise ValueError(
            "x must be between min and max (min={0}, x={1}, max={2})".format(
                min, x, max
            )
        )
    return min, max, x
