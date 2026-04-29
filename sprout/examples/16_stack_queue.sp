# 16 — Stack and Queue data structures

# Stack
fn make_stack() {
    return {"items": []}
}
fn stack_push(s, val) {
    append(s["items"], val)
}
fn stack_pop(s) {
    if len(s["items"]) == 0 {
        println("Error: stack underflow")
        return nil
    }
    return pop(s["items"])
}
fn stack_peek(s) {
    let items = s["items"]
    if len(items) == 0 { return nil }
    return items[len(items) - 1]
}
fn stack_empty(s) {
    return len(s["items"]) == 0
}

# Queue (using two stacks for O(1) amortized)
fn make_queue() {
    return {"inbox": [], "outbox": []}
}
fn queue_enqueue(q, val) {
    append(q["inbox"], val)
}
fn queue_dequeue(q) {
    if len(q["outbox"]) == 0 {
        while len(q["inbox"]) > 0 {
            append(q["outbox"], pop(q["inbox"]))
        }
    }
    if len(q["outbox"]) == 0 {
        println("Error: queue is empty")
        return nil
    }
    return pop(q["outbox"])
}

# Stack demo — balanced parentheses checker
fn is_balanced(expr) {
    let s = make_stack()
    let open  = {"(": ")", "[": "]", "{": "}"}
    let close_chars = ")}]"
    for i in range(len(expr)) {
        let ch = expr[i]
        if has(open, ch) {
            stack_push(s, ch)
        } else if contains(close_chars, ch) {
            if stack_empty(s) { return false }
            let top = stack_pop(s)
            if open[top] != ch { return false }
        }
    }
    return stack_empty(s)
}

println("'(()[]{})'  balanced?", is_balanced("(()[]{})"))
println("'([)]'      balanced?", is_balanced("([)]"))
println("'{[()]}'    balanced?", is_balanced("{[()]}"))

# Queue demo
let q = make_queue()
for i in range(1, 6) {
    queue_enqueue(q, i)
}
println("Dequeue order:")
let j = 0
while j < 5 {
    print(queue_dequeue(q), " ")
    j += 1
}
println("")
