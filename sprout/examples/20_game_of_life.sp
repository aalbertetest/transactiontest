# 20 — Conway's Game of Life (5 generations on a 10x10 grid)

let ROWS = 10
let COLS = 10

fn make_grid(rows, cols) {
    let grid = []
    let r = 0
    while r < rows {
        let row = []
        let c = 0
        while c < cols {
            append(row, 0)
            c += 1
        }
        append(grid, row)
        r += 1
    }
    return grid
}

fn copy_grid(grid) {
    let new_grid = make_grid(ROWS, COLS)
    let r = 0
    while r < ROWS {
        let c = 0
        while c < COLS {
            new_grid[r][c] = grid[r][c]
            c += 1
        }
        r += 1
    }
    return new_grid
}

fn count_neighbors(grid, row, col) {
    let count = 0
    let dr = -1
    while dr <= 1 {
        let dc = -1
        while dc <= 1 {
            if dr == 0 and dc == 0 {
                dc += 1
                continue
            }
            let nr = row + dr
            let nc = col + dc
            if nr >= 0 and nr < ROWS and nc >= 0 and nc < COLS {
                count += grid[nr][nc]
            }
            dc += 1
        }
        dr += 1
    }
    return count
}

fn step(grid) {
    let new_grid = copy_grid(grid)
    let r = 0
    while r < ROWS {
        let c = 0
        while c < COLS {
            let alive = grid[r][c]
            let n = count_neighbors(grid, r, c)
            if alive == 1 {
                if n < 2 or n > 3 {
                    new_grid[r][c] = 0
                }
            } else {
                if n == 3 {
                    new_grid[r][c] = 1
                }
            }
            c += 1
        }
        r += 1
    }
    return new_grid
}

fn print_grid(grid, gen) {
    println("Generation", gen)
    let r = 0
    while r < ROWS {
        let row_str = ""
        let c = 0
        while c < COLS {
            if grid[r][c] == 1 {
                row_str = row_str + "#"
            } else {
                row_str = row_str + "."
            }
            c += 1
        }
        println(row_str)
        r += 1
    }
    println("")
}

fn count_alive(grid) {
    let count = 0
    let r = 0
    while r < ROWS {
        let c = 0
        while c < COLS {
            count += grid[r][c]
            c += 1
        }
        r += 1
    }
    return count
}

# Glider pattern
let grid = make_grid(ROWS, COLS)
grid[1][2] = 1
grid[2][3] = 1
grid[3][1] = 1
grid[3][2] = 1
grid[3][3] = 1

let gen = 0
while gen < 5 {
    print_grid(grid, gen)
    println("  Alive cells:", count_alive(grid))
    grid = step(grid)
    gen += 1
}
