# 18 — Math operations and the math module

import math

println("pi =", math["pi"])
println("e  =", math["e"])

println("sin(pi/2) =", math["sin"](math["pi"] / 2))
println("cos(0)    =", math["cos"](0))
println("sqrt(2)   =", math["sqrt"](2))
println("log(e)    =", math["log"](math["e"]))

# Newton's square-root method (iterative)
fn newton_sqrt(n) {
    let guess = n / 2.0
    let i = 0
    while i < 50 {
        let next = (guess + n / guess) / 2.0
        if abs(next - guess) < 0.0000001 { break }
        guess = next
        i += 1
    }
    return guess
}

println("newton_sqrt(2)   =", newton_sqrt(2))
println("newton_sqrt(144) =", newton_sqrt(144))

# GCD and LCM
fn gcd(a, b) {
    while b != 0 {
        let tmp = b
        b = a % b
        a = tmp
    }
    return a
}
fn lcm(a, b) {
    return (a * b) / gcd(a, b)
}

println("gcd(48, 18) =", gcd(48, 18))
println("lcm(12, 18) =", lcm(12, 18))

# Sum of digits
fn digit_sum(n) {
    let s = str(n)
    let total = 0
    for i in range(len(s)) {
        total += int(s[i])
    }
    return total
}

println("digit_sum(9875) =", digit_sum(9875))
