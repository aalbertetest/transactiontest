# 05 — Arrays
let nums = [10, 20, 30, 40, 50]

println("Array:      ", nums)
println("Length:     ", len(nums))
println("First:      ", nums[0])
println("Last:       ", nums[4])

# Mutation
nums[2] = 99
println("After edit: ", nums)

# Append and pop
append(nums, 60)
println("After push: ", nums)
let last = pop(nums)
println("Popped:     ", last)
println("After pop:  ", nums)

# Nested arrays
let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
println("matrix[1][2] =", matrix[1][2])

# Iteration
let total = 0
for n in nums {
    total += n
}
println("Sum:", total)

# Array concatenation
let a = [1, 2]
let b = [3, 4]
println("Concat:", a + b)
