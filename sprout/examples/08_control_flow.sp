# 08 — Control flow: if/else, while, for, break, continue
let score = 85

# if / else if / else
if score >= 90 {
    println("Grade: A")
} else if score >= 80 {
    println("Grade: B")
} else if score >= 70 {
    println("Grade: C")
} else {
    println("Grade: F")
}

# While with break
let x = 0
while true {
    if x >= 5 { break }
    print(x, " ")
    x += 1
}
println("")

# For with continue (skip even numbers)
for i in range(10) {
    if i % 2 == 0 { continue }
    print(i, " ")
}
println("")

# Nested loops with break
let found = false
for i in range(5) {
    for j in range(5) {
        if i * j == 6 {
            println("Found:", i, "*", j, "= 6")
            found = true
            break
        }
    }
    if found { break }
}
