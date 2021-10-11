solve(Res) :-

 G=5,  %# 4. GC6K852
 D=2,  %# 5. GC6K88Z
 B=7,  %# 6. GC6KC4A
 E=4,  %# 7. GC6K9A9
 numlist(0, 9, Nums),
 numlist(0, 80, NList),
 
 member(A, NList),
 member(C, NList),
 member(F, NList),
 member(G, NList),
 
 
 C3 is C**(1/3),
 FH is B*B - B*G - sqrt(A) - D*E - C3,
 FI is (G*G + G*F - A - sqrt(A))/B * D,
 FJ is A*A - C*B - F*F - F*E - G + E,
 FK is G*F + C - B*F,
 FL is G*G + D*F +D*sqrt(A) - C3 - F*B - D - D**3,
 FM is (C*F + C*D + sqrt(A) + D*D - F*G)/E,
 FN is G*G - E*sqrt(A)*D + B,
 FO is F*F + E*E + sqrt(A+B) - G*G - D,

 H is round(FH), H >= 0, member(H, Nums),
 I is round(FI), I >= 0, member(I, Nums),
 J is round(FJ), J >= 0, member(J, Nums),
 K is round(FK), K >= 0, member(K, Nums),
 L is round(FL), L >= 0, member(L, Nums),
 M is round(FM), M >= 0, member(M, Nums),
 N is round(FN), N >= 0, member(N, Nums),
 O is round(FO), O >= 0, member(O, Nums),


 Res=[[0,H,I,J,K], [3, L, M, N, O], [A,C,F,G]].
