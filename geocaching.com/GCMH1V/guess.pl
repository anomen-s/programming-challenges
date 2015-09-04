
% XXX = 5406763 / ACEGI
% YY = 1280342 / BDFHA

% N50° 0(A+H).XXX'
% E014° EH.0YY'

solve(Res) :-

	numlist(1,9,N9),

%	I=7,
	E=2,
	select(I, N9, N8),
	
	select(A, N8, N7),
	select(B, N7, N6),
	select(C, N6, N5),
	select(D, N5, N4),
	select(E, N4, N3),
	select(F, N3, N2),
	select(G, N2, N1),
	select(H, N1, []),
	
	AH is A+H,
	member(AH, [7,8]),
	EH is E*10+H,
	member(EH, [24,25,26]),
	
	ACEGI is (((A*10+C)*10+E)*10+G)*10+I,
	BDFHA is (((B*10+D)*10+F)*10+H)*10+A,
	
	0 is (5406763 mod ACEGI),
	0 is (1280342 mod BDFHA),
	X is (5406763 / ACEGI),
	Y is (1280342 / BDFHA),
	X < 1000,
	Y < 100,
	
	Res=f(50,AH,X,14,EH,Y, c(A,B,C,D,E,F,G,H,I)).
	
