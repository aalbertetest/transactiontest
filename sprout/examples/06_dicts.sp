# 06 — Dictionaries
let person = {"name": "Alice", "age": 30, "city": "Tokyo"}

println("Name:", person["name"])
println("Age: ", person["age"])

# Mutation
person["age"] = 31
person["country"] = "Japan"
println("Updated:", person)

# Keys and values
println("Keys:  ", keys(person))
println("Values:", values(person))

# Membership check
println("Has 'name'?",    has(person, "name"))
println("Has 'email'?",   has(person, "email"))

# Iterate over keys
for k in keys(person) {
    println(k, "=>", person[k])
}

# Nested dicts
let config = {
    "db": {"host": "localhost", "port": 5432},
    "app": {"debug": true, "workers": 4}
}
println("DB host:", config["db"]["host"])
println("Workers:", config["app"]["workers"])
