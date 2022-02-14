load harness

@test "mytest-1" {
  check 'if false then x := 1 else w49 := 921' '⇒ w49 := 921, {}
⇒ skip, {w49 → 921}'
}

@test "mytest-2" {
  check 'if ¬ true then while true do skip else q2 := 70' '⇒ q2 := 70, {}
⇒ skip, {q2 → 70}'
}

@test "mytest-3" {
  check 'result := 1 * 57' '⇒ skip, {result → 57}'
}

@test "mytest-4" {
  check 'if 10 < 1 then lt := -30 + -33 else res := 1 + 9' '⇒ res := (1+9), {}
⇒ skip, {res → 10}'
}

@test "mytest-5" {
  check 'while false do skip' '⇒ skip, {}'
}
