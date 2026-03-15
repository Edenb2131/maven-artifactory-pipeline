package io.jfrog.example;

/**
 * Utility for formatting numbers — snapshot run 1 of 7.
 */
public class NumberFormatter {

    public static String toOrdinal(int n) {
        if (n <= 0) throw new IllegalArgumentException("Must be positive.");
        String[] suffixes = {"th","st","nd","rd"};
        int mod100 = n % 100;
        int mod10 = n % 10;
        String suffix = (mod100 >= 11 && mod100 <= 13) ? "th"
                      : (mod10 < suffixes.length) ? suffixes[mod10] : "th";
        return n + suffix;
    }

    public static String toBinary(int n) {
        return Integer.toBinaryString(n);
    }

    public static String toHex(int n) {
        return "0x" + Integer.toHexString(n).toUpperCase();
    }
}
