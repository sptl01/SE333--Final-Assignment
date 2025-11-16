package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    
    private Calculator calc = new Calculator();
    
    @Test
    public void testAdd() {
        assertEquals(5, calc.add(2, 3));
    }
    
    @Test
    public void testSubtract() {
        assertEquals(1, calc.subtract(3, 2));
    }

    @Test
    public void testMultiply() {
        assertEquals(6, calc.multiply(2, 3));
        assertEquals(0, calc.multiply(0, 5));
        assertEquals(-6, calc.multiply(-2, 3));
    }
    
    @Test
    public void testDivide() {
        assertEquals(2, calc.divide(6, 3));
        assertEquals(1, calc.divide(5, 5));
    }
    
    @Test
    public void testDivideByZero() {
        assertThrows(IllegalArgumentException.class, () -> calc.divide(5, 0));
    }
    
    @Test
    public void testIsEven() {
        assertTrue(calc.isEven(4));
        assertTrue(calc.isEven(0));
        assertFalse(calc.isEven(3));
        assertFalse(calc.isEven(-1));
    }
}