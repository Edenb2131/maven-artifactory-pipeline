package io.jfrog.example;

/**
 * Math utility class — added for snapshot run 3.
 */
public class MathUtils {

    public static int factorial(int n) {
        if (n < 0) throw new IllegalArgumentException("Input must be non-negative.");
        if (n == 0 || n == 1) return 1;
        return n * factorial(n - 1);
    }

    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    public static int fibonacci(int n) {
        if (n < 0) throw new IllegalArgumentException("Input must be non-negative.");
        if (n <= 1) return n;
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }
}
