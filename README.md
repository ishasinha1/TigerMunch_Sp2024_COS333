# TigerMunch_Sp2024_COS333

You must install certain packages into your cos333 virtual environment using the following
commands:

1. ```python -m pip install requests```
2. ```python -m pip install Pillow```
3. ```python -m pip install pillow_heif```

The following command exports the API key and sets an environment variable for the session. It must be run for the image module to function. 

This API key cannot appear in any publicly accessible document, or it will be deactivated.

```export OPENAI_API_KEY='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'```

If you are conducting testing that involves testing the API, you need to navigate to 'request_handler.py' and set the global variable 'testing_api' to 'True'

If you receive a 'SSLCertificateVerifyFailed' error after CAS authorization, run the following command:
```/Applications/Python\ 3.11/Install\ Certificates.command```

To run the app, run the following commands in your terminal once you've navigated to this
directory:

1. ```export APP_SECRET_KEY=<somesecretkey> ```
2. ```python runserver.py [port] ```


# I haven't removed these yet, since I'm still not 100% sure that we don't need them, but I don't think that we do
1. ```export FLASK_APP=backend.py```
2. ```export FLASK_ENV=development```
3. ```export APP_SECRET_KEY=<somesecretkey> ```
4. ```flask run```