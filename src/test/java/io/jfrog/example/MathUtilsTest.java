package io.jfrog.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathUtilsTest {

    @Test
    void testFactorial() {
        assertEquals(1, MathUtils.factorial(0));
        assertEquals(120, MathUtils.factorial(5));
    }

    @Test
    void testFactorialNegative() {
        assertThrows(IllegalArgumentException.class, () -> MathUtils.factorial(-1));
    }

    @Test
    void testIsPrime() {
        assertTrue(MathUtils.isPrime(7));
        assertFalse(MathUtils.isPrime(9));
        assertFalse(MathUtils.isPrime(1));
    }

    @Test
    void testFibonacci() {
        assertEquals(0, MathUtils.fibonacci(0));
        assertEquals(1, MathUtils.fibonacci(1));
        assertEquals(55, MathUtils.fibonacci(10));
    }
}
