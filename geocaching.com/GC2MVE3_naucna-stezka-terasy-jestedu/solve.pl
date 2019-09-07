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
 numlist(0, 9, Digits),

 A=20,
 B=4,
 C=0,
 D=10,
 E=1,
 F=3,
 I=1,
 J=9,

 member(A,[20,30,40]),
 member(E,[1,2,3]),
 member(F,[1,2,3]),
 member(I,[1,2,3]),
 member(J,[8,9,10]),

 member(G, [3,6,9]),
 member(H, [2,4,6]),

 N1 is 2*A+B+C, toDigits(N1, N1d), digitSum(N1d, N1s),
 N2 is G-F,
 N3 is H+I,
 N4 is D+E-J,

 E1 is 3*A+B-H, toDigits(E1, E1d), digitSum(E1d, E1s),
 E2 is D+E-G,
 E3 is J-C,member(E3, Digits),
 E4 is F-I, member(E4, Digits),

 59 is (5+N1s+N2+N3+N4 + 1+4+E1s+E2+E3+E4),

 Res = [[50,N1,N2,N3,N4], [14,E1,E2,E3,E4], [G, H]].
