# Copyright (c) 2020, CZ.NIC, z.s.p.o. (http://www.nic.cz/)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the CZ.NIC nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL CZ.NIC BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import collections.abc
import typing

from uci import Uci, UciExceptionNotFound

from . import boolean


def _is_iter(data):
    """Check if data is instance of iterable with exclusion of string as the only standard iterable type we handle."""
    return isinstance(data, collections.abc.Iterable) and not isinstance(data, str)


class NoDefaltType:
    """Type used to identify if there is some default provided to get method of EUci."""

    def __str__(self):
        return "NoDefault"


NoDefault = NoDefaltType()


class EUci(Uci):
    """Extended Uci wrapper"""

    def get(
        self,
        *args,
        dtype: type = str,
        convert: typing.Optional[typing.Callable[[typing.Any], typing.Any]] = None,
        list: bool = False,
        default: typing.Any = NoDefault,
    ):
        """Get configuration value.

        Up to three positional arguments are expected. Those are uci "config" "section" and "option" in this order.
        "config" is the only one that is really required.

        Dictionary with all sections is returned when only "config" is provided. If "section" and optionally also
        "option" is provided then it returns single value or tuple of values in case of lists.

        Following additional optional keywords arguments are available:
        dtype: data type to be returned. The supported is any type that can be initialized from string without
            additional parameters (such as int(str)). The default value is returned if error is raised on conversion and
            exception is logged to logging framework. The UciExceptionNotFound is raised if there is no default value.
        convert: the alternative to dtype. It is applied after dtype. It is not protected against the exception. It is
            expected to be a function that gets value as argument and should return convertion result.
        list: bool setting if option is expected to be list. This ensures that
            this method always returns tuple or on the other hand never
            returns one.
        default: default value to be returned instead of raising UciExceptionNotFound. Note that this value is returned
            as is without conversion. You have to ensure that it has same type as you expect.

        Note that dtype, convert and list are considered only if at least "section" is provided.

        When requested value is not found (including when it can't be converted) then this raises UciExceptionNotFound
        unless you specify default, in that case the default value is returned.
        """
        try:
            values = super().get(*args)
        except UciExceptionNotFound:
            if default is not NoDefault:
                return default
            raise
        if len(args) < 2:
            # Only "config" was provided, values is dictionary and no conversion is provided.
            return values

        def conv(value):
            try:
                result = boolean.VALUES[value.lower()] if dtype == bool else dtype(value)
            except Exception as exc:
                if default is not NoDefault:
                    return default
                raise UciExceptionNotFound from exc
            return convert(result) if convert is not None else result

        result = tuple(conv(str(value)) for value in (values if _is_iter(values) else (values,)))
        if not list:
            return result[0]
        return result

    @staticmethod
    def _set_value(value, dtype):
        if dtype == bool:
            return boolean.TRUE if value else boolean.FALSE
        return str(value)

    def set(self, *args):
        """Set configuration value.

        Up to three positional arguments specifying configuration can be
        specified. Those are "config", "section" and "option". Option does not
        have to be specified and in such case section value is set. Last
        positional argument (third or fourth one) is value to be set. This
        function automatically detect that argument type and sets value
        according to that. Supported types are: str, bool and int.
        If provided value is not of any of these types then it is converted to
        string.

        It is suggested to always explicitly type last positional argument to
        ensure correct type. That is in case of boolean for example:
        set("foo", "fee", "faa", bool(value))
        """
        if _is_iter(args[-1]):
            # We consider first value as authoritative for type
            dtype = type(args[-1][0]) if args[-1] else str
            super().set(*args[:-1], tuple((self._set_value(value, dtype) for value in args[-1])))
        else:
            super().set(*args[:-1], self._set_value(args[-1], type(args[-1])))
