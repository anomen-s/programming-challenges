% Pankrácké sochy
% try to guess missing numbers to compute final coordinantes

toDigits(Num, Digits) :- toDigits(Num, [], Digits).
toDigits(Num, DigitsIn, DigitsOut) :-
    Num > 0,
    NumD is (Num // 10), % integer division
    R is (Num mod 10),
    toDigits(NumD, [R|DigitsIn], DigitsOut).
toDigits(0, D, D).

digitSum([D0|Digits], Result) :-
    D0 < 10,D0 >= 0,
    digitSum(Digits, R),
    Result is D0 + R.
digitSum([], 0).

solve(Res) :-
 numlist(0, 20, N30),

 member(A, [6]),
 member(B, [2]),
 member(C, N30),
 member(D, N30),
 member(E, [2,5]),
 member(F, [3]),
 member(G, [20]),
 member(H, [6]),
 member(I, [4]),
 member(J, [3]),
 member(K, [9]),
 member(L, [10,20]),
 
 74 is A+B+C+D+E+F+G+H+I+J+K+L,
 X is ((H * I + J) * (E * G) + (G + J + K) * B),
 Y is (A * (D + F) * G * L + (C + G + K) * L - 1),
 X > 2000, X < 10000,
 Y > 4000, Y < 8000,
 toDigits(X, XXX), digitSum(XXX, XS),
 toDigits(Y, YYY), digitSum(YYY, YS),

 51 is 5+XS + 1+4+2+YS, 
 
 Res = [[50, 0, X, 14, 2, Y], [c,C],[d,D],[e,E],[l,L]].
