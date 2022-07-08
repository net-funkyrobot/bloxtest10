# MAKEFILE META

# Create stamps directory
.stamps:
	@mkdir -p $@


# GENERIC

# Run npm install (with firebase CLI as dev dependency)
node_modules: package.json
	npm i

# Flutter Dart pub get, gets Dart dependencies
--pubspec.lock: pubspec.yaml
	flutter pub get

# Flutter pub build runner (for initially creating generated files)
--build-runner-build:
	flutter pub run build_runner build --delete-conflicting-outputs


# INFRASTRUCTURE

# Create the Firebase project in a new Google Cloud project
.stamps/firebase-project.created.perm: | .stamps
	firebase projects:create net-startupworx-bloxtest10 -n BloxTest10 -o 956977996295 --non-interactive
	@touch $@

# Set the newly created Firebase project as default for this directory
.stamps/firebase-use.done: | .stamps .stamps/firebase-project.created.perm
	firebase use net-startupworx-bloxtest10 --non-interactive
	@touch $@

# Create an Android app in the new Firebase project
.stamps/firebase-app-android.created.perm: | .stamps .stamps/firebase-project.created.perm
	firebase apps:create -a net.startupworx.bloxtest10 ANDROID BloxTest10 --non-interactive
	@touch $@

# Create an iOS app in the new Firebase project
.stamps/firebase-app-ios.created.perm: | .stamps .stamps/firebase-project.created.perm
	firebase apps:create -b net.startupworx.bloxtest10 IOS BloxTest10 --non-interactive
	@touch $@

.stamps/infrastructure-setup.done: | .stamps/firebase-use.done .stamps/firebase-app-android.created.perm .stamps/firebase-app-ios.created.perm

infrastructure: | .stamps/infrastructure-setup.done
	echo "Infrastructure created"


# PREPARE

# Flutterfire configure. Generates dart code needed to initiialise Firebase in the Flutter app
lib/firebase_options.dart: | .stamps/infrastructure-setup.done
	flutterfire configure -p net-startupworx-bloxtest10 -a net.startupworx.bloxtest10 -i net.startupworx.bloxtest10 --platforms ios,android --yes

# Add additional things to the .gitignore file extra to what flutter create provides
# node_modules/
# .stamps/
# !.stamps/*.perm
--extra-gitignore:
	sed -i "" -e "s/^\.idea\//.idea\/\*/g" .gitignore
	echo "\n# Node/NPM/Firebase related\nnode_modules/\n\n# Makefile .stamps\n.stamps/*\n!.stamps/*.perm\n\n# IntelliJ Flutter run configurations\n!.idea/runConfigurations\n!.idea/runConfigurations/*\n" >> .gitignore

# Create a private GitHub repo and push all the initial files
.git: | --extra-gitignore
	git init
	gh repo create bloxtest10 --private --source=.
	git add -A && git commit -m "Initial commit" && git push -u origin main

# Libraries like Firestore require a higher iOS platform version than flutter create defaults to
.stamps/prepare-podfile.done: | .stamps
	sed -i "" -e "s/# platform :ios, '9.0'/platform :ios, '10.0'/g" ios/Podfile
	@touch $@

# Again Firestore requires a higher Android minimum SDK version than Flutter's default (21 instead of 16)
.stamps/prepare-build-gradle.done: | .stamps
	sed -i "" -e "s/ flutter\.minSdkVersion/ 21/g" android/app/build.gradle
	@touch $@

# Commit all the changes that the prepare target creates (stamp before commands are run so the stamp is included)
.stamps/prepare-changes-commit.done.perm: | .stamps
	@touch $@
	git add -A && git commit -m "Add initial make prepare changes" && git push -u origin main

.stamps/codebase-setup.done: | .git node_modules --pubspec.lock --build-runner-build lib/firebase_options.dart ios/Podfile .stamps/prepare-podfile.done .stamps/prepare-build-gradle.done .stamps/prepare-changes-commit.done.perm
	@touch $@

prepare: | .stamps/codebase-setup.done
	echo "Codebase setup completed"


# DEV

# Create Firebase emulators (currently just Firestore)
.stamps/firebase-emulators.created: | .stamps
	firebase setup:emulators:firestore
	@touch $@

dev: | --pubspec.lock lib/firebase_options.dart
	itermocil --here

dev-emulators: | .stamps/firebase-use.done .stamps/firebase-emulators.created --pubspec.lock lib/firebase_options.dart
	itermocil --here --layout itermocil_dev_emulators.yml


# DEPLOY

# Deploy changes in Firestore rules
deploy-rules:
	firebase deploy --only firestore:rules
