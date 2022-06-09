# BloxTest10

## Getting started post generation 🚀

Congratulations, you're leading the way! You'll create the backend infrastructure for this product.

### Step one: run `make prepare`

You have just generated this codebase using mason. Change into the project's root directory and run:

```
make prepare
```

This:

- Prepares a local NodeJS environment for running Firebase emulators and running a Firestore rules test suite.
- Gets Dart pub dependencies.
- Runs the `build_runner` to generate `freezed` and `json_serializable` code.
- Creates a Firebase project with an Android and iOS app
- Runs `flutterfire` CLI to create `firebase_options.dart` file with the Firebase app's credentials.

### Step two: add Firebase Auth identity providers

`firebase` CLI does not yet have this functionality so this step cannot be automated in `make prepare`.

Go to https://console.firebase.google.com/project/net-startupworx-bloxtest10/authentication/providers.

Add and enable at least the following identity providers:

- Anonymous
- Email/Password

Optionally you can add, enable and setup the following supported providers:

- Google
- Apple

Until you add the optional providers, sign-in via these methods will fail.

### Step three: Create Firestore database and deploy Firestore rules

This step requires upgrading the Firebase billing plan to "Blaze" (pay as you go) and therefore it cannot be automated (there is no CLI or API to do that).

Go to https://console.firebase.google.com/project/net-startupworx-bloxtest10/firestore/.

Click "Create database" and choose "production mode" (so that a closed rules set is used before we deploy our own rules). Choose a location to provision the cloud resources. Remember to note down the location as it is better to co-locate resources. Click "Enable".

Back in the project root, run:

```
make deploy-rules
```

### Step four: build and run the app for the first time

Via IntelliJ / Android Studio / command line, build and run the flutter app on any kind of device.

An iOS simulator or Android emulator will work fine too.

Ignore errors in the Dart code, this references missing l10n code which will be generated when the app is built for the first time.

## Getting started as a new developer 👩‍💻

You're a new developer joining this product, welcome!

You've just cloned the codebase, changed into the project's root directory. All you need to do is run:

```
make prepare
```

This:

- Prepares a local NodeJS environment for running Firebase emulators and running a Firestore rules test suite.
- Gets Dart pub dependencies.

DON'T WORRY running `make prepare` will not attempt to recreate the backend infrastructure for this product (as we'll already have the appropriate Makefile stamps in `.stamps/`).
