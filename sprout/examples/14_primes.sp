# 14 — Prime numbers: sieve of Eratosthenes and prime checking

fn is_prime(n) {
    if n < 2 { return false }
    if n == 2 { return true }
    if n % 2 == 0 { return false }
    let i = 3
    while i * i <= n {
        if n % i == 0 { return false }
        i += 2
    }
    return true
}

fn sieve(limit) {
    let composite = {}
    let primes = []
    let n = 2
    while n <= limit {
        if not has(composite, str(n)) {
            append(primes, n)
            let multiple = n * n
            while multiple <= limit {
                composite[str(multiple)] = true
                multiple += n
            }
        }
        n += 1
    }
    return primes
}

println("Primes up to 50:", sieve(50))
println("Total primes <= 100:", len(sieve(100)))

# First 10 primes
let count = 0
let candidate = 2
let first10 = []
while count < 10 {
    if is_prime(candidate) {
        append(first10, candidate)
        count += 1
    }
    candidate += 1
}
println("First 10 primes:", first10)

# Prime factorization
fn prime_factors(n) {
    let factors = []
    let d = 2
    while d * d <= n {
        while n % d == 0 {
            append(factors, d)
            n = n / d
        }
        d += 1
    }
    if n > 1 { append(factors, n) }
    return factors
}

println("Factors of 360:", prime_factors(360))
println("Factors of 100:", prime_factors(100))
