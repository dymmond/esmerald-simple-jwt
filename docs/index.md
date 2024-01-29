# Esmerald Simple JWT

<p align="center">
  <a href="https://esmerald.dev"><img src="https://res.cloudinary.com/dymmond/image/upload/v1673619342/esmerald/img/logo-gr_z1ot8o.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>The Simple JWT integration with Esmerald.</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/esmerald-simple-jwt/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/esmerald-simple-jwt/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald-simple-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald-simple-jwt?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald-simple-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald-simple-jwt.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://esmerald-simple-jwt.dymmond.com](https://esmerald-simple-jwt.dymmond.com) 📚

**Source Code**: [https://github.com/dymmond/esmerald-simple-jwt](https://github.com/dymmond/esmerald-simple-jwt)

**The official supported version is always the latest released**.

---

This package serves the purpose of facilitating a simple JWT integration of Esmerald and any application
that requires JWT.

Based on the standards and security explanations of the [official documentation](https://esmerald.dev/configurations/jwt/),
a simple jwt approach was designed to facilitate the life of the developers and **it is 100% custom**.

Esmerald Simple JWT aims to simplify the generation of the `access_token` and `refresh_token` by
providing out of the box mechanisms and views that can be imported directly into your application.

This package uses Pydantic for its own schemas.

## Installation

```shell
$ pip install esmerald-simple-jwt
```

## What does it bring

Esmerald Simple JWT comes with two different ways of using the package.

1. Via [Include](https://esmerald.dev/routing/routes/#include) where you can simply import directly
the views into your routing system.
2. Via [Pluggable](https://esmerald.dev/pluggables/) where the views can be installed into your
application.

This is not all what the packages brings for you. It also brings scaffolds for your custom backend
authentication and schemas to represent your token on response. All of this can be found in the
documentation and in more details.

## How does it work

It is very simple actually. Like everything in Esmerald can be done through the [settings](https://esmerald.dev/application/settings/),
this package wouldn't be any different.

In a nutshell, you will need to use the [SimpleJWT](./simple-jwt.md) configuration provided by
the package inside your settings and then import the urls into your package.

## Middleware

The Esmerald Simple JWT **does not come** with a middleware for any application and the reason for
this its because you can have your own custom middlewares and your own design without being forced
to use a specific one.

## Quickstart

For the sake of this example, [Edgy](https://esmerald.dev) will be used as ORM but feel free to
use your own and override anything you want and need.

What will we need?

* A [User model](#the-user-model). For this we will be using the [Edgy contrib from Esmerald](https://esmerald.dev/databases/edgy/models/)
since it provides already some out of the box configurations. Feel free to adapt it and use your own
models.
* A [backend authentication](#the-backend-authentication) allowing out user to be validated
for authentication.
* A [backend refresh](./backends.md#the-backend-refresh) that handles with the refresh token of the user
already logged in.
* A [SimpleJWT](#the-simple-jwt-configuration) configuration to be added to the application settings.

Both backend and refresh authentication will be using the default [Token](./token.md) from the
package.

### The user model

Esmerald provides already some out of the box integrations with databases like [Edgy](https://esmerald.dev/databases/edgy/models/)
but the package is not only strict to it. You can change and use whatever it suits you better.

This file will be placed in a `myapp/apps/accounts/models.py`.

```python title="myapp/apps/accounts/models.py"
{!> ../docs_src/quickstart/user.py !}
```

### The backend authentication

The [backend authentication](./backends.md#backend-authentication) does what the names suggests. Validates
and autenticates the user in the system and returns an `access_token` and `refresh_token`.

The backend authentication will be placed inside a `myapps/apps/accounts/backends.py`.

```python title="myapp/apps/accounts/backends.py"
{!> ../docs_src/quickstart/backend_auth.py !}
```

There is a lot to unwrap here right? Well, yes and no.

Although it looks very complex, in fact, it
is only using the [simple_jwt](./simple-jwt.md) settings to populate the necessary fields and get
some defaults from it such as `access_token_lifetime` and `refresh_token_lifetime` as well as
the names that will be displayed in the response for the tokens such as `access_token_name` and
`refresh_token_name`.

The rest is simple python logic to validate the login of a user.

### The backend refresh

The [backend refresh](./backends.md#backend-refresh) as the name suggests, serves the purpose of
refreshing the `access_token` from an existing `refresh_token` only.

The `RefreshAuthentication` on the contrary of the backend authentication, it is already provided
out of the box within **Esmerald Simple JWT** but you don't need to use it as well. Everything
can be customisable for your own needs.

The backend refresh will be placed inside a `myapps/apps/accounts/backends.py` as well.

```python title="myapp/apps/accounts/backends.py"
{!> ../docs_src/quickstart/backend_refresh.py !}
```

With the same principle of [backend authentication](#the-backend-authentication), it uses the
[SimpleJWT](./simple-jwt.md) configuration to populate the default values.

### The Simple JWT configuration

This is where we assemble the configurations for the package. The [SimpleJWT](./simple-jwt.md) is
placed inside your application settings file and then used by the application directly.

The configuration will be living inside `myapp/configs/settings.py`.

```python title="myapp/configs/settings.py"
{!> ../docs_src/quickstart/settings.py !}
```

Did you see how simple it was? Basically you just need to implement your own backend and refresh
backends and then import them into the [SimpleJWT](./simple-jwt.md) configuration.

!!! Danger
    The settings **must be called** `simple_jwt` or the application will fail to use the
    Esmerald Simple JWT package.

### Use the Esmerald Simple JWT

Now it is time to assemble the application and use the package.

As mentioned at the beginning, there are two different ways.

* Via [Include](#via-include) where you can simply import directly
the views into your routing system.
* Via [Pluggable](#via-pluggable) where the views can be installed into your
application.

#### Via Include

This is the simplest approach to almost every application in Esmerald.

```python
{!> ../docs_src/quickstart/via_include.py !}
```

#### Via Pluggable

This is the other way that Esmerald allows you to extend functionality. The pugglable will simply
install the package inside your application.

```python
{!> ../docs_src/quickstart/via_pluggable.py !}
```

### Starting and accessing the views

With everything assembled, we can now start our application but before
**we need to tell the application to use our custom settings**.

```shell
$ export ESMERALD_SETTINGS_MODULE=myapp.configs.settings.AppSettings
```

You can now start the application and access the endpoints via **POST**.

* `/auth/signin` - The login view to generate the `access_token` and the `refresh_token`.
* `/auth/refresh-access` - The refresh view to generate the new `access_token` from the `refresh_token`.

### OpenAPI

When Esmerald Simple JWT is added into your application, unless specified not to, it will add the
urls automatically to your OpenAPI documentation and so you can also access them via:

* `/docs/swagger` - The default OpenAPI url for the documentation of any Esmerald application.
