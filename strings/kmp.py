# Knuth-Morris-Pratt
# Performs search of pattern P in text T in O(|T| + |P|)
# see https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm

# returns first occurence of pattern P in given text
def find(pattern, text):
  if len(pattern) > len(text):
    return -1
  s = _comp_prefix_function(pattern + "\x00" + text)
  # iterate over [|pattern|, \pattern + '$' + text| - 1]
  for i in range(len(pattern) + 1, len(pattern) + len(text) + 1):
    if s[i] == len(pattern):
      return i - 2 * len(pattern)
  return -1

# returns list of all occurencies of pattern P in given text
def find_all(pattern, text):
  if len(pattern) > len(text):
    return []
  s = _comp_prefix_function(pattern + "\x00" + text)
  res = []
  # iterate over [|pattern|, \pattern + '$' + text| - 1]
  for i in range(len(pattern) + 1, len(pattern) + len(text) + 1):
    if s[i] == len(pattern):
      res.append(i - 2 * len(pattern))
  return res

def _comp_prefix_function(p):
  s = [ -1 for i in range(len(p)) ]
  s[0] = 0
  border = 0
  for i in range(1, len(p)):
    while border > 0 and p[i] != p[border]:
      border = s[border - 1]
    if p[i] == p[border]:
      border += 1
    else:
      border = 0
    s[i] = border
  return s