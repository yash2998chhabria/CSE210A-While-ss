load harness

@test "self-1" {
  check 'if x = 0 ∧ y < 4 then x := 14 else x := 7' '⇒ x := 14, {}
⇒ skip, {x → 14}'
}

@test "self-2" {
  check 'z := ( x8 + 2 ) * -4' '⇒ skip, {z → -8}'
}

@test "self-3" {
  check 'x := y - - - -2' '⇒ skip, {x → 2}'
}

@test "self-4" {
  check 'while false do x := x * z + k - 3 ' '⇒ skip, {}'
}

@test "self-5" {
  check 'if x = 0 ∧ 4 < 4 then x := 2 else x := 8' '⇒ x := 8, {}
⇒ skip, {x → 8}'
}