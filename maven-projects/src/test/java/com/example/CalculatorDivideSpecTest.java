package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorDivideSpecTest {

    private final Calculator calc = new Calculator();

    @Test
    public void dividesPositiveNumbers() {
        assertEquals(2, calc.divide(6, 3));
        assertEquals(0, calc.divide(1, 2)); // integer division truncates toward zero
    }

    @Test
    public void dividesNegativeNumbers() {
        assertEquals(-2, calc.divide(-6, 3));
        assertEquals(-2, calc.divide(6, -3));
        assertEquals(2, calc.divide(-6, -3));
    }

    @Test
    public void dividesWithRemainderTruncation() {
        assertEquals(2, calc.divide(7, 3));
        assertEquals(-2, calc.divide(-7, 3));
        assertEquals(-2, calc.divide(7, -3));
    }

    @Test
    public void divideByOneAndSelf() {
        assertEquals(5, calc.divide(5, 1));
        assertEquals(1, calc.divide(5, 5));
    }

    @Test
    public void divideByZeroThrows() {
        assertThrows(IllegalArgumentException.class, () -> calc.divide(5, 0));
        assertThrows(IllegalArgumentException.class, () -> calc.divide(0, 0));
    }
}
