Python UCI (Unified Configuration Interface) bindings
=====================================================
Bindings for OpenWRT configuration interface called UCI and specifically library
libuci.

You can use this library to access and set configuration from and to UCI.

Requirements
------------

* Python3
* libuci

Usage
-----
There are two primary packages in this project. There is `uci` and `euci`. In
most cases you want to use `euci` but because that is just a wrapper on top `uci`
please also read documentation for that as features you might be missing in `euci`
might be implemented there.

### uci
This is Python3 module and real wrapper on top of libuci. Its API is designed to
be same as the official Lua bindings but given by differences between these two
languages it is not completely same. Primarily some operations present in both are
more potent in pyuci.

General usage consist of initializing `Uci` handler, calling methods to modify or
receive configuration values and then committing it.
```python
from uci import Uci
u = Uci()
print(u.get("network"))
u.set("network", "lan", "type", "bridge")
u.commit("network")
```

`Uci` can also be used in Python `with` statement. This ensures that all changes
done to uci are committed on `with` statement context exit.
```python
with uci.Uci() as u:
	u.set("network", "lan", "type", "bridge")
```

#### uci.get(config, section, option)
Use this method if you want to get configuration values. Arguments are identifying
what you want to get. `config` is name of top level configuration file to read.
`section` is name of section (be aware that that is not type of section but
value). `option` is name of option or list. Only required argument is `config`.

This method returns different representations depending on number of provided
arguments.

When only `config` is provided then returned type is dictionary of dictionaries
with structure where first level keys are section values and values are
dictionaries with section content. The lower dictionary keys are then names of
options and lists. Value of option key is string and value of list key is tuple
containing strings.
```
{'lan': {'ifname': ('lan0', 'lan1', 'lan2', 'lan3', 'lan4'),
         'ipaddr': '192.168.1.1',
         'netmask': '255.255.255.0',
         'proto': 'static',
         'type': 'bridge'},
 'wan': {'ifname': 'eth2', 'proto': 'dhcp'}}
```
Note that Python3 ensures order in dictionaries and order in these are ensured to
be same as in configuration file. This is important for sections where order is
used to specify priority between for example rules.

When `section` and optionally also `option` are provided then only that specific
value is returned. In case of no `option` then type of section is returned as
string. If `option` is provided then it depends if it refers to list or to option.
If it is option then returned value is of string type. If it is list then tuple of
string is returned instead.

If any requested config, section or option are not found then
`UciExceptionNotFound` is thrown.

#### uci.get_all(config, section, option)
This is almost same as `uci.get` with only one difference. That is if you provide
only `config` and `section` then instead of getting section type it returns lower
dictionary same as if you provide only `config`. That is it returns dictionary
with all options and lists in that section.

#### uci.set(config, section, option, value)
Set given `value` to given option. Value has to be either string or table/tuple of
strings. If you provide string then value is set as option. If you provide
table/tuple then it is set as list. Note that it replaces previous value.

Note that section has to exists otherwise UciException is thrown.

This also allows you to set name for section (to create named section or change
name). Format of this function to be used for this is: `uci.set(config, section,
value)`.

#### uci.add(config, section_type)
Add a new anonymous section of type `section_type`. The auto-generated name of the
new section is returned.

#### uci.delete(config, section, option)
This method allows you to remove sections and options from configuration. `config`
and `section` are required. `option` is optional.

No error is reported if config, section or option does not exist.

Note that `section` in reality can be left out as well but in such case UCI does
nothing and no error is reported.

#### uci.rename(config, section, option, name)
This method allows you to rename existing option, list or section to different
name. `option` is optional and in such case section type is modified.

#### uci.reorder(config, section, index)
Move given section to different index in configuration file. All arguments are
required and `index` starts with 0.

#### uci.save(config, section, option)
Save changes deltas to save location. This does not modify configuration if self
but stores changes to specific configuration location. Using such delta you can
overlay configuration. See `uci.savedir()`, `uci.set_savedir()` and `uci`
initialization on how to set location for this delta save.

#### uci.commit(config, section, option)
Write changes to configuration files. You have to specify at least `config` but
you can also optionally specify more precise specification of `section` and
`option`. This ensures that anything outside of that specification is not written
to configuration.

#### uci.revert(config, section, option)
Drops all changes done on specified configuration. `config` argument is required
and `section` and `option` are optional and allows you to limit what is suppose to
be reverted.

#### uci.list_configs()
Returns list of all configs loaded and available to `Uci`.

#### uci.confdir()
Returns path to current configuration directory. This is directory where
configuration files are stored. This is suppose to be on permanent storage.

To set it you can either call `uci.set_confdir()` or to pass keyword `confdir`
argument to `Uci` initialization.

#### uci.set_confdir(path)
Sets given `path` as to be used as configuration directory. That is directory
that is used to load configuration from and store it to.

To get current configuration directory you can call `uci.confdir()`.

#### uci.savedir()
Returns path to current save directory. This is directory where delta files are
stored to. Those are changes done to configuration but not committed to
configuration directory yet. To update content of this directory you can call
`uci.save()`.

To set it you can either call `uci.set_savedir()` or to pass keyword `savedir`
argument to `Uci` initialization.

#### uci.set_savedir(path)
Sets given `path` as to be used as save directory. That is directory that is used
to store delta files. Those are files with configuration changes that are not
written to configuration files in configuration directory.

To get current save directory you can call `uci.savedir()`.

### euci (extended uci)
This is Python only extension for `uci` module. It extends `Uci` to `EUci` and
adds functionality like types to it.

General usage is same as in case of `Uci`. Every method you have in `Uci` you have
also access trough `EUci`. The only difference is that some methods are overloaded
and provide additional behavior on top of `Uci`.

`EUci` supports following types explicitly and any type that can be initialized
from string without additional info (such as __int__ or __float__):
* __str__: this is default and native UCI type.
* __bool__: this is boolean type that has only two states: `True` or `False`.
  UCI defines special strings that are suppose to be understood by all
  applications as booleans. Those are `0`, `no`, `off`, `false` and `disabled`
  for `False` and `1`, `yes`, `on`, `true`, `enabled` for `True`. Any other
  value in configuration is considered as invalid. `EUci` uses `0` and `1` if it
  sets this type.

#### euci.bolean.VALUES
This is dictionary mapping boolean strings to `True` or `False`.
Useful when getting whole config section and processing options individually.

#### euci.get(config, section, option, dtype=str, convert=None, list=False, default=NoDefault)
This is overloaded `uci.get` method. Three initial positional arguments are same
as in case of `uci.get` but behavior changes depending on additional keyword
arguments.

`dtype` is type that can be initialized from string passed as a single argument.
It ensures that returned value is always of given type. For list of supported
types please see previous section. The UciExceptionNotFound is raised if value
can't be converted to specified type.

`convert` can be a function that is called to do custom conversion. You can use
this if simple dtype is not enough for you. The reason for using this is to
convert to custom type or to provide additional info such as base to integer.
The function should accept value to convert as argument and return result.

`list` is bool specifying if `euci.get` should ensure that returned value is
considered as UCI option or as list. This is effectively difference between
returning value of `dtype` or tuple of `dtype` values. If configuration contains
UCI option with appropriate name but `list` is set to `True` then `euci.get`
returns tuple with value of that option. On the other hand if configuration
contains UCI list with appropriate name but `list` is set to `False` then
`euci.get` returns always value of type `dtype`. It returns first one if
multiple UCI lists were provided. The default is `False` so you should always
specify it as `True` when you are working with lists. Note that this keyword
has no effect if `section` is not provided. Meaning that in such case
dictionary is always returned.

`default` keyword argument can be used to suppress exception
`UciExceptionNotFound`. Instead of raising this exception `euci.get` returns
provided default. Note that default is never processed by conversion, so you
have to make sure that it is already of correct type or expect that it is might
not be. This has no effect if no `section` argument is provided. Meaning that
returned dictionary never contains anything else than strings as values.

#### euci.set(config, section, option, value)
This is overloaded `uci.set` method. It is not changed in form of how it is
called. You should not see any difference with exception of how it handles
`value`. It detects provided type of `value` argument and if it is one of
supported types then it converts it correctly to appropriate string
representation. Any unsupported type is considered to be string and string
conversion is performed.

`value` can be both only single value or tuple/list same as in case of `uci.set`.
In case of tuple/list it is expected that all values are of same type. That is
handled in way that value at index zero is used to detect type and rest of the
values are converted to that type.

### Examples
These are examples of different usage of `uci` and `euci` on OpenWRT system.

#### Getting configured host name
Hostname is in anonymous section of type `system`. We have to check all sections
to get correct name for that section.
```python
from euci import EUci
hostname = next(
    u.get("system", section, "hostname")
    for section in u.get("system")
    if u.get("system", section) == "system"))
```

Testing
-------
To run tests you need, on top of requirements, pytest.

You can use Docker to get appropriate environment for running tests (with pytest
and including libuci). Appropriate docker file can be found in this repository
with name `.Dockerfile`.

Running all tests is as easy as running: `python3 -m pytest tests`
