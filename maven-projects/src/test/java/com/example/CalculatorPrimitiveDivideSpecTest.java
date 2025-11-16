package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorPrimitiveDivideSpecTest {

    private final Calculator calc = new Calculator();

    @Test
    public void basicPositiveAndNegativeDivisions() {
        assertEquals(2, calc.divide(6, 3));
        assertEquals(0, calc.divide(1, 2));
        assertEquals(-2, calc.divide(-6, 3));
        assertEquals(-2, calc.divide(6, -3));
        assertEquals(2, calc.divide(-6, -3));
    }

    @Test
    public void remainderAndSignBehavior() {
        assertEquals(2, calc.divide(7, 3));
        assertEquals(-2, calc.divide(-7, 3));
        assertEquals(-2, calc.divide(7, -3));
        assertEquals(2, calc.divide(-7, -3));
    }

    @Test
    public void zeroNumeratorAndOneDivisor() {
        assertEquals(0, calc.divide(0, 5));
        assertEquals(5, calc.divide(5, 1));
        assertEquals(-5, calc.divide(5, -1));
    }

    @Test
    public void minValueDividedByMinusOne_overflowBehavior() {
        // Integer.MIN_VALUE / -1 overflows in two's complement arithmetic and results in Integer.MIN_VALUE
        assertEquals(Integer.MIN_VALUE, calc.divide(Integer.MIN_VALUE, -1));
    }

    @Test
    public void divideByZeroThrows() {
        assertThrows(IllegalArgumentException.class, () -> calc.divide(5, 0));
        assertThrows(IllegalArgumentException.class, () -> calc.divide(0, 0));
    }
}
