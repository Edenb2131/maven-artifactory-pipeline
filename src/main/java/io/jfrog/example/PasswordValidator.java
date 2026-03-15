package io.jfrog.example;

/**
 * Simple password validation utility — snapshot run 4 of 7.
 */
public class PasswordValidator {

    public static boolean isStrong(String password) {
        if (password == null || password.length() < 8) return false;
        boolean hasUpper   = password.chars().anyMatch(Character::isUpperCase);
        boolean hasLower   = password.chars().anyMatch(Character::isLowerCase);
        boolean hasDigit   = password.chars().anyMatch(Character::isDigit);
        boolean hasSpecial = password.chars().anyMatch(c -> "!@#$%^&*()_+-=".indexOf(c) >= 0);
        return hasUpper && hasLower && hasDigit && hasSpecial;
    }

    public static String strength(String password) {
        if (password == null || password.length() < 6) return "WEAK";
        if (isStrong(password)) return "STRONG";
        return "MEDIUM";
    }
}
