# 07 — Functions
fn greet(name) {
    return "Hello, " + name + "!"
}
println(greet("Alice"))

# Default parameters
fn power(base, exp = 2) {
    return base ** exp
}
println("3^2 =", power(3))
println("2^8 =", power(2, 8))

# Recursive function
fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}
println("10! =", factorial(10))

# First-class functions
fn apply(f, value) {
    return f(value)
}
fn double(x) { return x * 2 }
println("apply(double, 7) =", apply(double, 7))

# Anonymous function
let square = fn(x) { return x * x }
println("square(9) =", square(9))

# Closure
fn make_adder(n) {
    return fn(x) { return x + n }
}
let add5 = make_adder(5)
println("add5(10) =", add5(10))
println("add5(20) =", add5(20))
