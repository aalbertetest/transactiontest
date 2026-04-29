# 04 — String operations
let s = "Hello, Sprout!"

println("Length:   ", len(s))
println("Upper:    ", upper(s))
println("Lower:    ", lower(s))
println("Contains: ", contains(s, "Sprout"))
println("Replace:  ", replace(s, "Sprout", "World"))
println("Starts:   ", starts_with(s, "Hello"))
println("Ends:     ", ends_with(s, "!"))
println("Trim:     ", trim("  hello  "))

# String concatenation
let greeting = "Hello" + ", " + "world!"
println(greeting)

# String repetition
let line = "-" * 20
println(line)

# Split and join
let words = split("one two three", " ")
println(words)
println(join(words, "-"))

# Indexing
println("First char:", s[0])
println("Char at 7: ", s[7])
