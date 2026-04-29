# 17 — String processing utilities

fn count_words(s) {
    let words = split(trim(s), " ")
    let count = 0
    for w in words {
        if len(trim(w)) > 0 {
            count += 1
        }
    }
    return count
}

fn reverse_string(s) {
    let chars = []
    let i = len(s) - 1
    while i >= 0 {
        append(chars, s[i])
        i -= 1
    }
    return join(chars, "")
}

fn is_palindrome(s) {
    let lo = lower(trim(s))
    return lo == reverse_string(lo)
}

fn capitalize_words(s) {
    let words = split(s, " ")
    let result = []
    for word in words {
        if len(word) > 0 {
            let first = upper(word[0])
            let rest = ""
            let i = 1
            while i < len(word) {
                rest = rest + word[i]
                i += 1
            }
            append(result, first + rest)
        }
    }
    return join(result, " ")
}

fn count_char(s, ch) {
    let count = 0
    for i in range(len(s)) {
        if s[i] == ch { count += 1 }
    }
    return count
}

let text = "  the quick brown fox jumps over the lazy dog  "
println("Text:       ", trim(text))
println("Words:      ", count_words(text))
println("Vowels:     ", count_char(lower(text), "a") +
                        count_char(lower(text), "e") +
                        count_char(lower(text), "i") +
                        count_char(lower(text), "o") +
                        count_char(lower(text), "u"))
println("Capitalized:", capitalize_words(trim(text)))

println("Palindromes:")
let words = ["racecar", "hello", "level", "world", "madam", "sprout"]
for w in words {
    println(" ", w, "->", is_palindrome(w))
}
