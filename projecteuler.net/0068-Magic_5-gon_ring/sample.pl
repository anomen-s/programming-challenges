

solve(Res) :-
    numlist(1,6, Nums0),
    
    select(A1, Nums0, Nums1),
    select(A2, Nums1, Nums2),
    select(A3, Nums2, Nums3),
    SUM is A1+A2+A3,
    select(A4, Nums3, Nums4), A4>A1,
    A6 is SUM-A3-A4,
    select(A6, Nums4, Nums5),
    A7 is SUM-A2-A6, A7>A1,
    select(A7, Nums5, []),
    
    Res=[[A1,A2,A3],[A4,A3,A6],[A7,A6,A2]].

    
    
    