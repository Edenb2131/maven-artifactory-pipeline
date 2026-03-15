package io.jfrog.example;

import java.util.List;
import java.util.Optional;

/**
 * Collection utility class — snapshot run 3 of 7.
 */
public class CollectionUtils {

    public static <T extends Comparable<T>> Optional<T> max(List<T> list) {
        if (list == null || list.isEmpty()) return Optional.empty();
        return list.stream().max(Comparable::compareTo);
    }

    public static <T extends Comparable<T>> Optional<T> min(List<T> list) {
        if (list == null || list.isEmpty()) return Optional.empty();
        return list.stream().min(Comparable::compareTo);
    }

    public static <T> List<T> flatten(List<List<T>> nested) {
        if (nested == null) return List.of();
        return nested.stream().flatMap(List::stream).toList();
    }
}
