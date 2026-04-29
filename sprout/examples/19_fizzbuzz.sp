# 19 — FizzBuzz and variations

fn fizzbuzz(n) {
    if n % 15 == 0 { return "FizzBuzz" }
    if n % 3  == 0 { return "Fizz" }
    if n % 5  == 0 { return "Buzz" }
    return str(n)
}

# Classic 1-20
for i in range(1, 21) {
    println(fizzbuzz(i))
}

println("---")

# Generalised: collect results
fn run_fizzbuzz(limit) {
    let results = []
    for i in range(1, limit + 1) {
        append(results, fizzbuzz(i))
    }
    return results
}

let fb = run_fizzbuzz(30)
let fizz_count = 0
let buzz_count = 0
let fizzbuzz_count = 0

for val in fb {
    if val == "FizzBuzz" { fizzbuzz_count += 1 }
    else if val == "Fizz" { fizz_count += 1 }
    else if val == "Buzz" { buzz_count += 1 }
}

println("In range 1-30:")
println("  Fizz:     ", fizz_count)
println("  Buzz:     ", buzz_count)
println("  FizzBuzz: ", fizzbuzz_count)
