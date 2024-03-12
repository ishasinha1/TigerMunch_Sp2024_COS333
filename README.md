# TigerMunch_Sp2024_COS333

You must install the requests package into your cos333 virtual environment:

python -m pip install requests

The following command exports the API key and sets an environment variable for the session. It must be run for the image module to function. 

This API key cannot appear in any publicly accessible document, or it will be deactivated!!!

export OPENAI_API_KEY='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'

To run the app, run the following commands in your terminal once you've navigated to this
directory:

1. export FLASK_APP=backend.py
2. export FLASK_ENV=development
3. flask run