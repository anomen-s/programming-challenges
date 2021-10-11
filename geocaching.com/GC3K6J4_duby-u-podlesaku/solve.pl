solve(Res) :-
    numlist(0,9,Nums),

    
 A=4,
 %B=6,
 C=6,
 E=3,
 F=9,

 member(E, [1,2,3,4,5,6]),
 member(F, [8,9]),
 member(B, [5,6,7]),
 member(D, Nums), D < 7,
 member(G, [1,3]),

 %#D=6,  # 1968, nevychází výpočet
 %G=3, %# nebo jen 1 nezamalovaná?
 
 % N 50°02.FEC E 014°35(A+G)(B-1)(D+3) 
 
 AG is A+G,AG < 10,
 B1 is B-1,
 D3 is D+3, D3 < 10,
 
 Sum is A+B+C+D+E+F+G,
 
 Sum=37,
 Res=[[F,E,C],[AG,B1,D3]].
 
