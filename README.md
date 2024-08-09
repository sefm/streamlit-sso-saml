# streamlit-sso-saml
streamlit SSO SAML integration workaround 

Option 1: Using pysaml2 with xmlsec
```
pip install pysaml2 xmlsec Flask
```
Configure saml_config.py

Option 2: Nginx Reverse Proxy
```
sudo apt-get update
sudo apt-get install nginx
```

Option 2: use nextjs or react to handle this
```
npm install passport-saml express-session body-parser express
```
Create a saml.js file in your project to configure Passport.js for SAML authentication:

```
const passport = require('passport');
const SamlStrategy = require('passport-saml').Strategy;
const fs = require('fs');

passport.use(new SamlStrategy(
  {
    path: '/login/callback',
    entryPoint: 'https://{yourOktaDomain}/sso/saml',
    issuer: 'http://localhost:3000',
    cert: fs.readFileSync('./path-to-okta-public-cert.pem', 'utf-8'),
  },
  function(profile, done) {
    return done(null, profile);
  }
));

passport.serializeUser(function(user, done) {
  done(null, user);
});

passport.deserializeUser(function(user, done) {
  done(null, user);
});

module.exports = passport;
```

Set Up Express Server to Handle SAML Authentication:

For Next.js: Create a server.js file:

```const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const passport = require('./saml');

const next = require('next');
const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  const server = express();

  server.use(bodyParser.urlencoded({ extended: false }));
  server.use(session({ secret: 'secret', resave: false, saveUninitialized: true }));
  server.use(passport.initialize());
  server.use(passport.session());

  server.get('/login', passport.authenticate('saml', { failureRedirect: '/', failureFlash: true }));

  server.post('/login/callback',
    passport.authenticate('saml', { failureRedirect: '/', failureFlash: true }),
    function(req, res) {
      res.redirect('/');
    }
  );

  server.get('*', (req, res) => {
    return handle(req, res);
  });

  server.listen(3000, (err) => {
    if (err) throw err;
    console.log('> Ready on http://localhost:3000');
  });
});
```

For Next.js, add a next.config.js file:

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8501/:path*',
      },
    ];
  },
};
```
For React, add the proxy field in your package.json:

```
"proxy": "http://localhost:8501",
```
Run
```
node server.js
```
Note your app inthis case wont need samlpy xmlsec
```
streamlit run your_streamlit_app.py
```
