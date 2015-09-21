# Example for Kompassi OAuth2 SSO

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

The rest of this README needs update.

## Getting started

First, make sure `kompassi.dev` and `ssoexample.dev` resolve to localhost via `/etc/hosts`:

    127.0.0.1 localhost kompassi.dev ssoexample.dev

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
    git clone https://github.com/tracon/kompassi-oauth2-example.git
    cd kompassi-oauth2-example
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py runserver 127.0.0.1:8001
    iexplore http://ssoexample.dev:8001

When you click the "Go to protected page" link, you should be transferred to your Kompassi development instance. Log in with user `mahti` and password `mahti`, authorize the example application to receive your user info, and you should see the protected page.

## Configuration

```python
AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

KOMPASSI_OAUTH2_AUTHORIZATION_URL = 'http://kompassi.dev:8000/oauth2/authorize'
KOMPASSI_OAUTH2_TOKEN_URL = 'http://kompassi.dev:8000/oauth2/token'
KOMPASSI_OAUTH2_CLIENT_ID = 'kompassi_insecure_test_client_id'
KOMPASSI_OAUTH2_CLIENT_SECRET = 'kompassi_insecure_test_client_secret'
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = 'http://kompassi.dev:8000/api/v2/people/me'
```

## Development gotchas

### "OAuth2 MUST use HTTPS"

Technically it's horribly wrong to use OAuth2 over insecure HTTP. However, it's tedious to set up TLS for development. That's why we monkey patch `oauthlib.oauth2:is_secure_transport` on `DEBUG = True`. See `kompassi_oauth2_example/settings.py`.

### Applications on `localhost` in different ports share the same cookies

1. Run Kompassi at `localhost:8000`
2. Run this example `localhost:8001`
3. Try to log in

Expected results: You are logged in

Actual results: 500 Internal Server Error due to session not having `oauth_state` in `/oauth2/callback`

Explanation: Both applications share the same set of cookies due to cookies being matched solely on the host name, not the port

Workaround: Add something like this to `/etc/hosts` and use `http://kompassi.dev:8000` and `http://ssoexample.dev:8001` instead.

    127.0.0.1 localhost kompassi.dev ssoexample.dev

## License

    The MIT License (MIT)

    Copyright (c) 2014–2015 Santtu Pajukanta

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
