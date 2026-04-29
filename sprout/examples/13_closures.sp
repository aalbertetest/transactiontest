# 13 — Closures and function factories

fn make_counter(start) {
    let count = start
    fn increment() {
        count += 1
        return count
    }
    return increment
}

let c1 = make_counter(0)
let c2 = make_counter(100)
println(c1())   # 1
println(c1())   # 2
println(c2())   # 101
println(c1())   # 3

# Memoization via dict closure
fn memoize(f) {
    let cache = {}
    return fn(n) {
        let key = str(n)
        if has(cache, key) {
            return cache[key]
        }
        let result = f(n)
        cache[key] = result
        return result
    }
}

fn slow_fib(n) {
    if n <= 1 { return n }
    return slow_fib(n - 1) + slow_fib(n - 2)
}

let fast_fib = memoize(slow_fib)
println("fib(10) =", fast_fib(10))

# Partial application
fn partial(f, first_arg) {
    return fn(x) { return f(first_arg, x) }
}

fn add(a, b) { return a + b }
let add10 = partial(add, 10)
println("add10(5) =", add10(5))
println("add10(99) =", add10(99))
