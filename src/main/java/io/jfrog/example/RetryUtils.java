package io.jfrog.example;

import java.util.concurrent.Callable;

/**
 * Utility for retrying operations — snapshot run 7 of 7.
 */
public class RetryUtils {

    public static <T> T retry(Callable<T> task, int maxAttempts) throws Exception {
        if (maxAttempts < 1) throw new IllegalArgumentException("maxAttempts must be >= 1");
        Exception last = null;
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return task.call();
            } catch (Exception e) {
                last = e;
            }
        }
        throw last;
    }

    public static void retryVoid(Runnable task, int maxAttempts) {
        Exception last = null;
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                task.run();
                return;
            } catch (Exception e) {
                last = e;
            }
        }
        if (last != null) throw new RuntimeException("All " + maxAttempts + " attempts failed", last);
    }
}
