// Consistent padding
const kstPaddingUnit = 8.0;


// Firestore collections

const kstUsersColl = "users";
const kstTransactionsColl = "transactions";


// Firestore paths

String user(String uid) => "$kstUsersColl/$uid";


// Route paths

// Sign in app
const kstSignInHomeScreen = "/";
const kstEmailPasswordSignUpScreen = "/sign-up";

// Home app
const kstHomeScreen = "/";
const kstSettingsScreen = "/home/settings";
const kstInfoScreen = "/home/info";
const kstDeveloperMenuScreen = "/home/developer-menu";
