enum UserProfile {
  scout,
  manager,
  systemAdmin,
}

enum ManagerType {
  productionManager,
  sprayCoordinator,
  regionalManager,
  system,
}

class UserSession {
  static UserProfile currentProfile = UserProfile.scout;

  static ManagerType? currentManagerType;

  static String currentUser = '';
}
