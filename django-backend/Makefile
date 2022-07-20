# MAKEFILE META

# Create stamps directory
.stamps:
	@mkdir -p $@


# GENERIC

# Run pip install (both main and dev dependencies)
.PHONY: | python-dependencies
python-dependencies:
	pip install -r requirements.txt && pip install -r requirements-dev.txt


# PREPARE

# Install Cloud SQL proxy via gcloud CLI
.stamps/gcloud-cloud-sql-proxy.installed: | .stamps
	gcloud components install cloud_sql_proxy --quiet
	@touch $@

firebase-admin-service-account.json:
	gcloud secrets versions access latest --secret firebase_admin_service_account_key > firebase-admin-service-account.json

.stamps/codebase-setup.done: | .stamps/gcloud-cloud-sql-proxy.installed firebase-admin-service-account.json
	@touch $@

.PHONY: | prepare
prepare: | .stamps/codebase-setup.done
	echo "Codebase setup completed"


# INFRASTRUCTURE

# Enable Google Cloud sqladmin.googleapis.com API
# TODO: param here
.stamps/gcloud-apis.enabled.perm: | .stamps
	gcloud services enable sqladmin.googleapis.com secretmanager.googleapis.com --project net-startupworx-bloxtest10 --quiet
	@touch $@

# Create Google Cloud SQL Postgres database instance
# TODO: param here
.stamps/gcloud-cloud-sql-instance.created.perm: | .stamps .stamps/gcloud-apis.enabled.perm
	gcloud sql instances create net-startupworx-bloxtest10-postgres --project net-startupworx-bloxtest10 --database-version POSTGRES_13 --tier db-f1-micro --region europe-west1 --quiet
	@touch $@

# Create Postgres database on new instance
# TODO: param here
.stamps/gcloud-cloud-sql-database.created.perm: | .stamps .stamps/gcloud-cloud-sql-instance.created.perm .stamps/gcloud-cloud-sql-instance.created.perm
	gcloud sql databases create bloxtest10 --instance net-startupworx-bloxtest10-postgres --project net-startupworx-bloxtest10 --quiet
	@touch $@

# Create Postgres database user on new instance
# TODO: param here
# TODO: create secure random password (and print it out) in mason pre-hook
.stamps/gcloud-cloud-sql-database-user.created.perm: | .stamps .stamps/gcloud-cloud-sql-database.created.perm
	gcloud sql users create bloxtest10 --instance net-startupworx-bloxtest10-postgres --password somelongpassword123 --project net-startupworx-bloxtest10 --quiet
	@touch $@

# Create django secrets file (sensitive settings variables) in Google Cloud Secret Manager
# TODO: param here
.stamps/gcloud-secrets.created.perm: | .stamps
	gcloud secrets create backend_settings --data-file .env --project net-startupworx-bloxtest10 --quiet
	rm -rf .env
	gcloud secrets add-iam-policy-binding backend_settings --member serviceAccount:net-startupworx-bloxtest10@appspot.gserviceaccount.com --role roles/secretmanager.secretAccessor --project net-startupworx-bloxtest10 --quiet
	@touch $@

.stamps/gcloud-firebase-admin-service-account-key.created.perm: | .stamps
	gcloud iam service-accounts keys create firebase-admin-service-account.json --iam-account=firebase-adminsdk-9og4c@net-startupworx-bloxtest10.iam.gserviceaccount.com --quiet --project net-startupworx-bloxtest10
	gcloud secrets create firebase_admin_service_account_key --data-file firebase-admin-service-account.json --project net-startupworx-bloxtest10 --quiet
	@touch $@

.stamps/infrastructure-setup.done: | .stamps .stamps/gcloud-apis.enabled.perm .stamps/gcloud-cloud-sql-database-user.created.perm .stamps/gcloud-secrets.created.perm .stamps/gcloud-firebase-admin-service-account-key.created.perm
	@touch $@

.PHONY: | infrastructure
infrastructure: | .stamps/infrastructure-setup.done
	echo "Infrastructure created"


# DEV

.PHONY: | secrets
secrets:
	echo "Getting latest environment settings and secrets from Google Cloud Secret Manager"
	gcloud secrets versions access latest --secret backend_settings > .secrets

.PHONY: | deploy-secrets
deploy-secrets:
	gcloud secrets versions add backend_settings --data-file .secrets

# Run Django devserver via Cloud SQL proxy
.PHONY: | dev
dev: | .stamps/codebase-setup.done python-dependencies
	itermocil --here