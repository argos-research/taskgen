# Dict to XML Translation

In general, task blocks, tasks, task-sets and admission control data are
represented as Python `dict` object. Since the `genode-taskloader` is the
primary target platform, all objects are parsed to the XML format by `genode.*`
sessions.  Due to this fact, not every `dict` object is a valid object and might
contain invalid key-value pairs. The translation is done by the
[xmltodict](https://github.com/martinblech/xmltodict) library.

## XML-Attributes

Attributes are translated with `@` prefix.

```XML
<root>
    <element has="an attribute"></element>
</root>
```

```Python
{
    "root" : {
        "element" : {
            "@has" : "an attribute"
        }
}
```

## Multiple Elements

Multiple XML elements are represented as Python `list`.

```XML
<root>
    <element>one</element>
    <element>one more</element>
</root>
```

```Python
{
    "root" : {
        "element" : [
            "one",
            "one more"
        ]
}
```
