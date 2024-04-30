# TigerMunch_Sp2024_COS333

Welcome to TigerMunch, a transformative web application that revolutionizes nutrition tracking! With TigerMunch, users can simply upload a photo and/or description of their meal. This data is then processed by GPT-4, which estimates the caloric and macronutrient content of each meal.

TigerMunch enables users to monitor their daily nutritional intake against their personalized goals and view their nutritional trends over time through intuitive charts and graphs. Dive into a smarter way to track your nutrition with TigerMunch!

You must install certain packages into your cos333 virtual environment using the following commands:

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

Using the API consumes credits. To prevent unnecessary usage, our backend is configured to return default values instead of making API requests by default. The global variable 'testing_api' in the file 'request_handler.py' controls this behavior and is set to 'False'. If you need to test the API during your testing, change this variable to 'True'.

Furthermore, we've retained a deprecated feature that utilizes GPT-4 to generate personalized consumption trends. This feature is disabled by default but can be activated for testing or demonstration purposes. To enable it, set the global variable 'generate_descriptions' to 'True' in 'request_handler.py'. This will print the generated trends on your terminal every time you visit the homepage.

To run the app, run the following commands in your terminal once you've navigated to this directory:

macOS
1. ```export APP_SECRET_KEY=33333``` (random secret key for ease copy-pasting)
2. ```export DATABASE_URL='postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database'```
3. ```export POSTMARK_API_KEY='ae2f1172-778b-4577-bc2a-7b5f56ab2958'```
4. ```export OPENAI_API_KEY='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'```
4. ```python runserver.py [port]```


If you receive a 'SSLCertificateVerifyFailed' error after CAS authorization, run the following command in your terminal:
```/Applications/Python\ 3.11/Install\ Certificates.command```

Windows
1.  in powershell ```$env:APP_SECRET_KEY='<somesecretkey>'```
2. in commandprompt ```setx APP_SECRET_KEY "<somesecretkey>"```
3.  in powershell ```$env:DATABASE_URL='postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database'```
4. in commandprompt ```setx DATABASE_URL "postgres://tiger_munch_database_user:XTZfrY8uas1J2rQK66ZBdOlw73bjUofb@dpg-cnpnit7109ks738phqqg-a.ohio-postgres.render.com/tiger_munch_database"```
5. in powershell ```$env:POSTMARK_API_KEY='ae2f1172-778b-4577-bc2a-7b5f56ab2958'```
6.  in powershell ```$env:OPENAI_API_KEY='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'```
7. in commandprompt ```setx OPENAI_API_KEY "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"```
8.  ```python runserver.py [port] ```


If you receive a 'SSLCertificateVerifyFailed' error after CAS authorization, run the following command in your terminal:
```/Applications/Python\ 3.11/Install\ Certificates.command```
