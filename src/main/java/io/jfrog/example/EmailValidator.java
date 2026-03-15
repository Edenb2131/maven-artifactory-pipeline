package io.jfrog.example;

import java.util.regex.Pattern;

/**
 * Simple email validation utility — snapshot run 6 of 7.
 */
public class EmailValidator {

    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    public static boolean isValid(String email) {
        if (email == null || email.isBlank()) return false;
        return EMAIL_PATTERN.matcher(email).matches();
    }

    public static String extractDomain(String email) {
        if (!isValid(email)) throw new IllegalArgumentException("Invalid email: " + email);
        return email.substring(email.indexOf('@') + 1);
    }
}
