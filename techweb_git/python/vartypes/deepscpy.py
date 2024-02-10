#Si consiglia l'esecuzione di questo esempio su:
#https://pythontutor.com/

l_originale = [ "a" , "b", "c i a o".split(), 4 ]

print(l_originale)

#reference copy
l_ref_copy = l_originale

l_originale[0] = "z"

print("Le due liste sono \"uguali\"? " +   ("SI" if l_ref_copy is l_originale else "NO"))
print(id(l_ref_copy))
print(id(l_originale))

print(l_ref_copy)

#shallow copy
l_shallow_cpy = l_originale.copy()

l_originale[2][0] = "m"

print("Le due liste sono \"uguali\"? " +   ("SI" if l_shallow_cpy is l_originale else "NO"))
print(id(l_shallow_cpy))
print(id(l_originale))
print(l_shallow_cpy)

#deep copy
import copy
l_deep_cpy = copy.deepcopy(l_originale)

l_originale[2][0] = "x"

print("Le due liste sono \"uguali\"? " +   ("SI" if l_deep_cpy is l_originale else "NO"))
print(id(l_deep_cpy))
print(id(l_originale))
print(l_deep_cpy)


