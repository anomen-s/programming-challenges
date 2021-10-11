solve(Res):-
    
    % nekompletni
    
    numlist(0,9, Digit),
    numlist(0,19, Digits20),
    numlist(0,59, Digits60),
    numlist(20,30, EDigits),
    
    G=5, %# 7) počet tabulek
    I=8, %# 9 c) běžných suvenýrů
    K=1, %# 11 a) mezi reklamními plochami
    L=9, %# 12 c) mořská panna
    M=3, %# 13) TS 2563 (streetview)
    P=14, %# 16) č.o. (streetview)
    R=20, %# 18) značka (streetview)
    S=3, %# 19) ryby (streetview)
    U is R-P-G+I, member(U, Digit),
    %print(['U',U]),nl,

    O=0, % guess, %member(O, Digit),

    !,
    member(F, [30,26]),

    member(E, Digits60),
    member(H, Digit), 
    H > 0, % ciferace

    T is E-O-F-H-K, member(T, Digit),
    %print(['T',T]),nl,

    member(J, Digits20),
    J > 0, % pravdepodobne.

    ZZ is J/(4*S), member(ZZ, Digit),
    %print(['ZZ',ZZ]),nl,

    member(D, [18,20,22,24,26]),
    %print(['D',D]),nl,


    member(A, [5,10]),
    %print(['A',A]),nl,

    Z is (K+D+A)/(A+K), member(Z, Digit),

    member(B, [1,2,3,4,5]),

    W is (E/L)+B, member(W, Digit),
    %print(['W',W]),nl,

    member(N, [1,5,9]),

    Y is N-M, member(Y, Digit),
    
    member(Q, [6,4]),
    %print(['Q',Q,'N',N]),nl,

    V is Q-B, member(V, Digit),

    member(C, Digits60), C > 9, Cm is C mod 2, Cm = 0,
    X is (F/B)+C-(H/I), member(X, EDigits),

    X >= 23, X =< 27, %guess

    % guess
    T >= 6,

    Res=[[50,O,T,U,V,W], [14,X,Y,Z,ZZ]].
    %print([A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S]).
    