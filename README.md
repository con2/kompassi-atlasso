# OAuth2 to Atlassian Crowd SSO adapter for Kompassi

**Problem**: Kompassi now lives at [kompassi.eu](https://kompassi.eu) but we need to do cookie based authentication for Atlassian products at eg. [confluence.tracon.fi](https://confluence.tracon.fi).

**Solution**: Rip all Crowd related code from Kompassi into an external application that authenticates against Kompassi using OAuth2.

So basically

1. Try to access a protected resource under `confluence.tracon.fi`
2. Get redirected to `https://atlasso.tracon.fi/crowd`
3. Notice you have no session, get redirected to `https://atlasso.tracon.fi/oauth2/login`
4. OAuth2 session is setup, get redirected to `https://kompassi.eu/oauth2/authorize`
5. Notice you have no session, get redirected to `https://kompassi.eu/login`
6. Log in using whatever method you like
7. Get redirected via `https://atlasso.tracon.fi/oauth2/callback` to `https://atlasso.tracon.fi/crowd`
8. Get a cookie, get redirected to `https://confluence.tracon.fi`

## Getting started

First, make sure `kompassi.dev` and `atlassodev.tracon.fi` resolve to localhost via `/etc/hosts`:

    127.0.0.1 localhost kompassi.dev atlassodev.tracon.fi

Next, install and run development instance of [Kompassi](/tracon/kompassi) if you don't yet have one:

    virtualenv venv-kompassi
    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi.git
    cd kompassi
    pip install -r requirements.txt
    ./manage.py setup --test
    ./manage.py runserver 127.0.0.1:8000
    iexplore http://kompassi.dev:8000

`./manage.py setup --test` created a test user account `mahti` with password `mahti` in your Kompassi development instance.

Now, in another terminal, install and run this example:

    source venv-kompassi/bin/activate
    git clone https://github.com/tracon/kompassi-atlasso.git
    cd kompassi-atlasso
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://atlassodev.tracon.fi:8001

When you click the "Go to protected page" link, you should be transferred to your Kompassi development instance. Log in with user `mahti` and password `mahti`, authorize the example application to receive your user info, and you should see the protected page.

## Configuration

You need an OAuth2 application in Kompassi (get it from the admin UI) and an application in Crowd (get it from the setup UI). See `atlasso/settings.py`.

## Development gotchas

### "OAuth2 MUST use HTTPS"

Technically it's horribly wrong to use OAuth2 over insecure HTTP. However, it's tedious to set up TLS for development. That's why we monkey patch `oauthlib.oauth2:is_secure_transport` on `DEBUG = True`. See `kompassi_oauth2_example/settings.py`.

### Applications on `localhost` in different ports share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this example `localhost:8001`
3. Try to log in

**Expected results**: You are logged in

**Actual results**: 500 Internal Server Error due to session not having `oauth_state` in `/oauth2/callback`

**Explanation**: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

**Workaround**: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://atlassodev.tracon.fi:8001` instead.

    127.0.0.1 localhost kompassi.dev atlassodev.tracon.fi

### Cookie domain must match that of Crowd and Confluence

For the client app to see the `crowd.token_key` cookie, it needs to be in the `tracon.fi` domain.

**That** is why we picked `atlassodev.tracon.fi` above, not eg. `atlasso.dev`.

For your development pleasure, `kompassidev.tracon.fi` deals out cookies that do not have the "secure" flag set so that you don't need to access your development instance via HTTPS.

### Validation factors

Crowd requires that you use the same validation factors for refreshing the session as you did for setting the session up. The validation factors used in our installation are as follows:

* `remote_address`: Always `127.0.0.1`.
* `X-Forwarded-For`: The public, Internet-facing IP address of the browser.

In `settings.py` there are lambdas that are used to extract this information from the request object. What the lambdas should do depends on your setup:

#### Production installation behind a reverse proxy

It is recommended to install Django apps behind an Apache or nginx proxy. In this case, `REMOTE_ADDR` is always `127.0.0.1` and the real IP address is in the `X-Forwarded-For` HTTP header.

```python
KOMPASSI_CROWD_VALIDATION_FACTORS = {
    'remote_address': lambda request: '127.0.0.1',
    'X-Forwarded-For': lambda request: request.META['HTTP_X_FORWARDED_FOR'],
}
```

#### Production or development installation without a proxy

If the Django instance is not behind a proxy and sees your public, Internet-facing IP address in `REMOTE_ADDR`, you should fake being behind a proxy as our Crowd, Confluence etc. installations **are** behind a proxy.

```python
KOMPASSI_CROWD_VALIDATION_FACTORS = {
    'remote_address': lambda request: '127.0.0.1',
    'X-Forwarded-For': lambda request: request.META['REMOTE_ADDR'],
}
```

NB. The Django development server is not suitable for use in production, but you might use `gunicorn` or `uwsgi`.

#### Development server in a private IP address or localhost

If your development server does not get your Internet-facing IP address in either `X-Forwarded-For` or `REMOTE_ADDR`, you need to fake it in the validation factors. This is usually the case for local development setups where you have the Django instance running in either `localhost` or a (virtual) machine behind a NAT.

```python
KOMPASSI_CROWD_VALIDATION_FACTORS = {
    'remote_address': lambda request: '127.0.0.1',
    'X-Forwarded-For': lambda request: '84.248.69.106', # the Internet-facing IP address of your browser
}
```

## License

    The MIT License (MIT)

    Copyright © 2014–2016 Santtu Pajukanta

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
