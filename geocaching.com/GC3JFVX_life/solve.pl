solve(Res) :-
	A=50, % wiki -  Dani Reese
	B=0, % wiki -  Olivia
	H=14, % from coords
	I=2, % from coords
	G=43, % http://www.aceshowbiz.com/tv/episodeguide/life_s1_e07/
	F=11, % http://www.aceshowbiz.com/tv/episodeguide/life_s1_e06/
	D=9, % http://www.aceshowbiz.com/tv/episodeguide/life_s1_e04/
	L=58, % http://www.aceshowbiz.com/tv/episodeguide/life_s1_e10/
	
	member(C, [3,4]),
	member(D, [3,6,9]),
	member(E, [8,6,7]),
	member(F, [10,11,12]),
	member(G, [47, 43, 37]),
	member(H, [15,14]),
	member(I, [1,2,3]),
	member(J, [3,6]),
	member(K, [34, 22, 25]),
	member(L, [26, 49, 58]),
	member(M, [49, 36, 18]),
	member(N, [69, 77, 42]),

	303 is A + B + C + D + E + F + G + H + I + J + K + L + M + N,
	DEFG is  D * E * F + G,
	DEFG < 1000,
	KLMN is K + L + M + N,
	KLMN < 1000,
	Res = [[A,B,C,D,E,F,G,H,I,J,K,L,M,N], (A, [B,C], DEFG), e(H,[I,J], KLMN)].
	
