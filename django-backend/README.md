# BloxTest10 backend

## Getting started post generation 🚀

When you want to create backend infrastructure, come here and initialize it from `django-backend/Makefile`.

### Step one: run `make prepare`

This will:

- Install the Google Cloud SQL Proxy via the `gcloud cli`

TODO: This shouldn't be in prepare?

- Obtain the required secrets

```
make prepare
```

### Step two: run `make infrastructure`

This will:

- Enable the required Google APIs
- Create a managed PostgreSQL database instance, database and user via Google Cloud SQL
- Create the required keys and secrets and store them in Secret Manager

```
make infrastructure
```

### Step three: run `make deploy`

This will make the first deployment of the app to AppEngine

### Step four: Enable and configure Identity-Aware Proxy (IAP)

Go to the following page on the Google Cloud Console:

https://console.cloud.google.com/security/iap?serviceId=default&project=net-startupworx-bloxtest10

Enable IAP on the App Engine app.
