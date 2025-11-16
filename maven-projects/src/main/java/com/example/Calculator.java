package com.example;

public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int multiply(int a, int b) {
        return a * b;
    }
    
    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
    
    public boolean isEven(int n) {
        return n % 2 == 0;
    }

    // Null-checking overloads for caller convenience (throw NPE with clear message)
    public int add(Integer a, Integer b) {
        if (a == null || b == null) throw new NullPointerException("add: operands must not be null");
        return add(a.intValue(), b.intValue());
    }

    public int subtract(Integer a, Integer b) {
        if (a == null || b == null) throw new NullPointerException("subtract: operands must not be null");
        return subtract(a.intValue(), b.intValue());
    }

    public int multiply(Integer a, Integer b) {
        if (a == null || b == null) throw new NullPointerException("multiply: operands must not be null");
        return multiply(a.intValue(), b.intValue());
    }

    public int divide(Integer a, Integer b) {
        if (a == null || b == null) throw new NullPointerException("divide: operands must not be null");
        return divide(a.intValue(), b.intValue());
    }

    public boolean isEven(Integer n) {
        if (n == null) throw new NullPointerException("isEven: parameter must not be null");
        return isEven(n.intValue());
    }
}