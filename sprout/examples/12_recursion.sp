# 12 — Recursion: towers of Hanoi, flatten, binary search

fn hanoi(n, from, to, via) {
    if n == 1 {
        println("Move disk 1 from", from, "to", to)
        return nil
    }
    hanoi(n - 1, from, via, to)
    println("Move disk", n, "from", from, "to", to)
    hanoi(n - 1, via, to, from)
}

println("Towers of Hanoi (3 disks):")
hanoi(3, "A", "C", "B")
println("")

# Flatten nested arrays (one level)
fn flatten(arr) {
    let result = []
    for item in arr {
        if type(item) == "array" {
            for x in item {
                append(result, x)
            }
        } else {
            append(result, item)
        }
    }
    return result
}

let nested = [[1, 2], [3, 4], [5, [6, 7]]]
println("Nested:    ", nested)
println("Flattened: ", flatten(nested))

# Binary search
fn binary_search(arr, target) {
    let lo = 0
    let hi = len(arr) - 1
    while lo <= hi {
        let mid = (lo + hi) / 2
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            lo = mid + 1
        } else {
            hi = mid - 1
        }
    }
    return -1
}

let sorted = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
println("Array:", sorted)
println("Search 23 at index:", binary_search(sorted, 23))
println("Search 99 at index:", binary_search(sorted, 99))
