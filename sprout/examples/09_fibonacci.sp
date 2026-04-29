# 09 — Fibonacci sequence (recursive and iterative)

fn fib_recursive(n) {
    if n <= 1 { return n }
    return fib_recursive(n - 1) + fib_recursive(n - 2)
}

fn fib_iterative(n) {
    if n <= 1 { return n }
    let a = 0
    let b = 1
    let i = 2
    while i <= n {
        let tmp = a + b
        a = b
        b = tmp
        i += 1
    }
    return b
}

println("Fibonacci (recursive):")
for i in range(10) {
    print(fib_recursive(i), " ")
}
println("")

println("Fibonacci (iterative):")
for i in range(10) {
    print(fib_iterative(i), " ")
}
println("")

println("fib(30) =", fib_iterative(30))
