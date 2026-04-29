# 10 — Sorting algorithms: Bubble Sort and Insertion Sort

fn bubble_sort(arr) {
    let n = len(arr)
    let i = 0
    while i < n - 1 {
        let j = 0
        while j < n - i - 1 {
            if arr[j] > arr[j + 1] {
                let tmp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = tmp
            }
            j += 1
        }
        i += 1
    }
    return arr
}

fn insertion_sort(arr) {
    let n = len(arr)
    let i = 1
    while i < n {
        let key = arr[i]
        let j = i - 1
        while j >= 0 and arr[j] > key {
            arr[j + 1] = arr[j]
            j -= 1
        }
        arr[j + 1] = key
        i += 1
    }
    return arr
}

let data1 = [64, 34, 25, 12, 22, 11, 90]
let data2 = [64, 34, 25, 12, 22, 11, 90]

println("Original:       ", data1)
println("Bubble sort:    ", bubble_sort(data1))
println("Insertion sort: ", insertion_sort(data2))
