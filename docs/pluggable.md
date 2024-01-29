# Pluggable

The Pluugable object is the one of the ways of importing the Esmerald Simple JWT into your Esmerald
application via *installation* of the package.

```python
{!> ../docs_src/quickstart/via_pluggable.py !}
```

Esmerald [official documentation abuot Pluggables](https://esmerald.dev/pluggables/) goes into
great detail about how to use it and when to use it.

In other words, what Esmerald Simple JWT pluggable does is to simple install a [ChildEsmerald](https://esmerald.dev/routing/router/#child-esmerald-application)
module inside the Esmerald application using the pluggable itself.

Since Esmerald is modular, it could be inside the main Esmerald application or inside any nested
Esmerald or ChildEsmerald objects.

It is your choice.

## API Reference

You can check all the available parameters to use with this simple configuration in the
[Pluggable API Reference](./references/pluggable.md).
