# 15 — Linked list implemented with dicts

fn make_node(value, next) {
    return {"value": value, "next": next}
}

fn list_push(head, value) {
    return make_node(value, head)
}

fn list_to_array(head) {
    let arr = []
    let node = head
    while node != nil {
        append(arr, node["value"])
        node = node["next"]
    }
    return arr
}

fn list_length(head) {
    let count = 0
    let node = head
    while node != nil {
        count += 1
        node = node["next"]
    }
    return count
}

fn list_reverse(head) {
    let prev = nil
    let current = head
    while current != nil {
        let next_node = current["next"]
        current["next"] = prev
        prev = current
        current = next_node
    }
    return prev
}

fn list_contains(head, target) {
    let node = head
    while node != nil {
        if node["value"] == target { return true }
        node = node["next"]
    }
    return false
}

# Build a list: 5 -> 4 -> 3 -> 2 -> 1 -> nil
let head = nil
for i in range(1, 6) {
    head = list_push(head, i)
}

println("List:     ", list_to_array(head))
println("Length:   ", list_length(head))
println("Contains 3?", list_contains(head, 3))
println("Contains 9?", list_contains(head, 9))

head = list_reverse(head)
println("Reversed: ", list_to_array(head))
