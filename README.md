# Django CRM Project - Contact Management Project 

## Live Demo - http://professionalcipher.pythonanywhere.com/ 
[Comment on Youtube Video if not working & i will fix it] [Installation Video](https://youtu.be/A6mTN6G-adM)

I am trying to create a Tutorial on How yo Create CRM or Contact Management System in Django. Basically this tutorial is creating while explaining video tutorial. This is the series of Django CRM Tutorial.

![Image of CRM](https://studygyaan.com/wp-content/uploads/2020/02/Django-CRM-Website.jpg)

### Setup
1. Create a folder and put all the files inside it.
2. Create a virtual environtment - `virtualenv env`
3. Activate VirtualENV - ubuntu : `source env/bin/activate` || windows : `. .\env\Scripts\activate`
4. Run requirements.txt - `pip install -r requirements.txt`
5. Run the Application - `python manage.py runserver`
6. Migrate


## Required secret configuration

Before starting the app, supply `DJANGO_SECRET_KEY` and `SOCIAL_AUTH_FACEBOOK_SECRET` in the process environment through your deployment's secret manager or secure local environment configuration. Both values are required and must be non-empty. The Facebook backend is enabled, so its secret is required even if you have not used Facebook login yet. Django does not automatically load a .env file in this project.

Generate a new random Django signing key privately, install the same value on all web and worker instances, and restart them together. Replace the exposed Facebook app secret in Meta's developer dashboard and then update the deployment environment. Existing installations that relied only on `crm_main/local_settings.py` must move these two settings into the environment; the environment signing key takes precedence over that file.

Never reuse the exposed values, commit replacement keys, or retain a compromised signing key as a fallback. Removing a value from the latest code does not remove Git history or revoke it at its provider. Signing-key rotation can invalidate signed sessions and password-reset links; user account passwords do not change.

Run the dependency-free configuration regression checks with:

```bash
python -m unittest discover -s tests -p 'test_security_config.py' -v
```

These checks use synthetic secrets and stub the Django messages import. They do not replace the application's deployment checks.
