package io.jfrog.example;

/**
 * Utility for numeric range checking — snapshot run 5 of 7.
 */
public class RangeChecker {

    public static boolean inRange(double value, double min, double max) {
        return value >= min && value <= max;
    }

    public static double clamp(double value, double min, double max) {
        if (min > max) throw new IllegalArgumentException("min must be <= max");
        return Math.max(min, Math.min(max, value));
    }

    public static double normalize(double value, double min, double max) {
        if (min == max) throw new IllegalArgumentException("min and max must differ");
        return (value - min) / (max - min);
    }
}
