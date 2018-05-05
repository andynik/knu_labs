% use SWI-Prolog (https://swish.swi-prolog.org) for compiling
% find more examples in https://pro-prof.com/archives/845


%%% to reverse a list

rev([], []) :- !.

rev([H|T], X) :-
    !,
    rev(H, NewH),
    rev(T, NewT),
    append(NewT, [NewH], X).

rev(X, X).

?- rev([1, 2, 3], X)
% X = [3, 2, 1]


%%% to zip two lists

zip([], [], []).
zip([X|Xs], [Y|Ys], [X,Y|Zs]) :- zip(Xs,Ys,Zs).

?- zip([1, 2, 3], [4, 5, 6], X)
% X = [1, 4, 2, 5, 3, 6]


%%% to append two lists

append([], List, List).
append([Head|Tail], List, [Head|Rest]) :-
    append(Tail, List, Rest).

?- append([1, 2, 3],[4, 5, 6], L)
% L = [1, 2, 3, 4, 5, 6]


%%% to remove an element from every list in set of lists

del_el(X, [X|Z], Y) :-
    del_el(X, Z, Y).

del_el(X, [V|Z], [Q|Y]) :-
    X \== V,
    del_el(X, V, Q),
    del_el(X, Z, Y).

del_el(X, [], []).
del_el(X, Y, Y).

?- del_el([2], [2, 1, [3, 2], 4], D)
% D = [1, [3], 4]
