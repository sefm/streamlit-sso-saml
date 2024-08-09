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
