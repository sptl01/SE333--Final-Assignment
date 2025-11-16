package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorNullChecksTest {

    private final Calculator calc = new Calculator();

    @Test
    public void addNullsThrow() {
        assertThrows(NullPointerException.class, () -> calc.add((Integer)null, Integer.valueOf(1)));
        assertThrows(NullPointerException.class, () -> calc.add(Integer.valueOf(1), (Integer)null));
        assertThrows(NullPointerException.class, () -> calc.add((Integer)null, (Integer)null));
    }

    @Test
    public void divideNullsThrow() {
        assertThrows(NullPointerException.class, () -> calc.divide((Integer)null, Integer.valueOf(1)));
        assertThrows(NullPointerException.class, () -> calc.divide(Integer.valueOf(1), (Integer)null));
    }

    @Test
    public void isEvenNullThrows() {
        assertThrows(NullPointerException.class, () -> calc.isEven((Integer)null));
    }

    @Test
    public void nonNullOverloadsWork() {
        assertEquals(5, calc.add(Integer.valueOf(2), Integer.valueOf(3)));
        assertEquals(6, calc.multiply(Integer.valueOf(2), Integer.valueOf(3)));
        assertEquals(2, calc.subtract(Integer.valueOf(5), Integer.valueOf(3)));
        assertEquals(2, calc.divide(Integer.valueOf(6), Integer.valueOf(3)));
        assertTrue(calc.isEven(Integer.valueOf(4)));
    }

    @Test
    public void subtractNullsThrow() {
        assertThrows(NullPointerException.class, () -> calc.subtract((Integer)null, Integer.valueOf(1)));
        assertThrows(NullPointerException.class, () -> calc.subtract(Integer.valueOf(1), (Integer)null));
    }
}
