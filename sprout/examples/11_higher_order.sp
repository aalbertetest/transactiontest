# 11 — Higher-order functions: map, filter, reduce

fn map(arr, f) {
    let result = []
    for item in arr {
        append(result, f(item))
    }
    return result
}

fn filter(arr, pred) {
    let result = []
    for item in arr {
        if pred(item) {
            append(result, item)
        }
    }
    return result
}

fn reduce(arr, f, init) {
    let acc = init
    for item in arr {
        acc = f(acc, item)
    }
    return acc
}

let nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

let doubled = map(nums, fn(x) { return x * 2 })
println("Doubled:  ", doubled)

let evens = filter(nums, fn(x) { return x % 2 == 0 })
println("Evens:    ", evens)

let total = reduce(nums, fn(acc, x) { return acc + x }, 0)
println("Sum:      ", total)

let product = reduce(nums, fn(acc, x) { return acc * x }, 1)
println("Product:  ", product)

# Chain: sum of squares of even numbers
let result = reduce(
    map(filter(nums, fn(x) { return x % 2 == 0 }),
        fn(x) { return x * x }),
    fn(a, b) { return a + b },
    0
)
println("Sum of squares of evens:", result)
