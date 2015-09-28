%We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.
%
%The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.
%
%Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
%HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
%
%observations:
%xxx*xxx > xxx - invalid
%xxx* xx = xxxx - ok
% xx* xx < xxxxx - invalid

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% consult('solve.pl').
% solve(Result).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

selectMult(List, Num, [E| Result], Rem) :-
    Num > 0,
    select(E, List, Rest),
    Num1 is Num-1,
    selectMult(Rest, Num1, Result, Rem).

selectMult(Rem, 0, [], Rem).

selectNumber(List, Num, Result, Remainder) :-
    selectMult(List, Num, ResultList, Remainder),
    atomic_list_concat(ResultList, NumStr),
    atom_number(NumStr, Result).


solve([Prod, Res]) :-
    assert(s([])),
    % select product
    numlist(1, 9, Nums),
    selectNumber(Nums, 4, Prod, Rem),
    
    member(N1, [1,2]),
    selectNumber(Rem, N1, F1, Rem2),
    
    N2 is 5 - N1,
    selectNumber(Rem2, N2, F2, []),
    Prod is F1*F2,
    
    s(R),
    retract(s(R)),
    assert(s([Prod|R])),
    
    compute(Res).


removeDupes([],[]).
removeDupes([Last],[Last]).
removeDupes([M1,M1|R],R2) :- removeDupes([M1|R], R2).
removeDupes([M1,M2|R],[M1|R2]) :- M1 =\= M2, removeDupes([M2|R], R2).

compute([RawList, Sum]) :-
	s(RawList),
	sort(RawList, DupList),
	removeDupes(DupList, RList),
	sumlist(RList, Sum).
