enum UserProfile {
  scout,
  manager,
  systemAdmin,
}


class UserSession {
  static UserProfile currentProfile = UserProfile.scout;


  static String currentUser = '';
}
