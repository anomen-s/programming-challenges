

% in Prague
% N 50°(ADxDCA-72)/1000 E 014°(ABxADxBC+10)/1000


digitSum([D0|Digits], Result) :-
         integer(D0), D0 >= 0,
         digitSum(Digits, R),
         digitSum(D0, R0),
         Result is R0 + R.
digitSum(N, Result) :-
         integer(N), N > 0,
         ND is (N // 10),
         NR is (N mod 10),
         digitSum(ND, R),
         Result is NR + R.
digitSum([], 0).
digitSum(0, 0).



solve([[A,B,C,D],[N,E]]) :-
    numlist(0, 9, Nums),
    member(A, Nums),
    member(B, Nums),
    member(C, Nums),
    member(D, Nums),
    N is (A*10+D) * (D*100+C*10+A) - 72,
    E is (A*10+B) * (A*10+D) * (B*10+C) + 10,

    N > 1000,
    N < 8000,
    E > 24000,
    E < 32000,

%    print([A,B,C,D]),
%    print([N,E]),nl,

    digitSum([514, N, E],53).
    
%53 is 5 + N + 1+4+E
