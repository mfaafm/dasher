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


def get_min_max_value(minimum, maximum, value=None, step=None):
    """Return min, max, value given input values with possible None."""
    # Either min and max need to be given, or value needs to be given
    if value is None:
        if minimum is None or maximum is None:
            raise ValueError(
                "unable to infer range, value from: ({0}, {1}, {2})".format(
                    minimum, maximum, value
                )
            )
        diff = maximum - minimum
        value = minimum + (diff / 2)
        # Ensure that value has the same type as diff
        if not isinstance(value, type(diff)):
            value = minimum + (diff // 2)
    else:  # value is not None
        if not isinstance(value, Real):
            raise TypeError("expected a real number, got: %r" % value)
        # Infer min/max from value
        if value == 0:
            # This gives (0, 1) of the correct type
            vrange = (value, value + 1)
        elif value > 0:
            vrange = (-value, 3 * value)
        else:
            vrange = (3 * value, -value)
        if minimum is None:
            minimum = vrange[0]
        if maximum is None:
            maximum = vrange[1]
    if step is not None:
        # ensure value is on a step
        tick = int((value - minimum) / step)
        value = minimum + tick * step
    if not minimum <= value <= maximum:
        raise ValueError(
            "value must be between min and max (min={0}, value={1}, max={2})".format(
                minimum, value, maximum
            )
        )
    return minimum, maximum, value
