# TigerMunch_Sp2024_COS333

You must install certain packages into your cos333 virtual environment using the following
commands:

macOS
1. ```python -m pip install requests```
2. ```python -m pip install Pillow```
3. ```python -m pip install pillow_heif```
4. ```python -m pip install pytz```
5. ```brew update```
6. ```brew install libpq```
7. ```brew link --force libpq```
8. ```python -m pip install psycopg2``` (If this does not work, try: ```python -m pip install psycopg2-binary```)

Windows
1. ```python -m pip install requests```
2. ```python -m pip install Pillow```
3. ```python -m pip install pillow_heif```
4. ```python -m pip install pytz```
5.  install lib libpq library -- https://www.postgresql.org/download/
6.  password:12312, port:5000
8. ```python -m pip install psycopg2``` (If this does not work, try: ```python -m pip install psycopg2-binary```)

The following command exports the API key and sets an environment variable for the session. It must be run for the image module to function. 

This API key cannot appear in any publicly accessible document, or it will be deactivated.

macOS

```export OPENAI_API_KEY='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'```

Windows 
1.  in powershell ```$env:OPENAI_API_KEY='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'```
11. in commandprompt ```setx OPENAI_API_KEY "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"```

If you are conducting testing that involves testing the API, you need to navigate to 'request_handler.py' and set the global variable 'testing_api' to 'True'

If you receive a 'SSLCertificateVerifyFailed' error after CAS authorization, run the following command:
```/Applications/Python\ 3.11/Install\ Certificates.command```

To run the app, run the following commands in your terminal once you've navigated to this
directory:

macOS
1. ```export APP_SECRET_KEY=33333``` (random secret key for ease copy-pasting)
2. ```export DATABASE_URL='postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database'```
3. ```export POSTMARK_API_KEY='ae2f1172-778b-4577-bc2a-7b5f56ab2958'```
4. ```python runserver.py [port] (optional)[True] ```
(if you wish to test with API requests, set the optinal command line argument to True, otherwise, do nothing)

Windows
1.  in powershell ```$env:APP_SECRET_KEY='<somesecretkey>'```
11. in commandprompt ```setx APP_SECRET_KEY "<somesecretkey>"```
2.  in powershell ```$env:DATABASE_URL='postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database'```
22. in commandprompt ```setx DATABASE_URL "postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database"```
3. in powershell ```$env:POSTMARK_API_KEY='ae2f1172-778b-4577-bc2a-7b5f56ab2958'```
4.  ```python runserver.py [port] ```
