def count_occurrences(matrix, element):
      # Converte a matriz para uma lista de números
  numbers = [num for row in matrix for num in row]
  # Conta quantas vezes o elemento aparece na lista
  return numbers.count(element)



matrix = [[0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
print (count_occurrences(matrix,2))


# retorna 1