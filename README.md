# python-webpage-watchdog
A simple application that, using an MD5 hash of webpage data, will notify a user if a specific webpage has changed since the last run.

# How to use:
- Set the URL
- Optionally update the SOUP_FIND_ALL_CONDITION variable to find something on a page that would be useful to monitor for changes
- Optionally set the username and password variables for basic authentication - leave empty if you don't need them
- Run the app once to configure the initial hash of the site.
- Up to you how you want to continue to run the app.
   - Windows you could run it on startup of your PC. Or you could setup a service that runs the script every few hours.
   - Mac you can setup a cronjob or even launchd for more control
   - Linux you could use a cronjob

# venv
Its recommend you use a virtual Python environment as this disconnects the packages installed to run this script from your main Python environment

To create a venv run the following command from this repo: `python3 -m venv ./venv`

This will create a new virtual environment in the `venv` directory. You can then source this directory to run using that environment (VS Code does this for you)
