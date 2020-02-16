import re 

class BoolStringSolver():
  
  '''
  Main method: solve_string(string, num_var, var_names = [])
  
    string: bool logic string in python-like format
      examples: 'x_1 or x_2 and x_3', '(not (x_1 or x_3) or x_1) and x_2'
      important: bool varaibles nums must starts from 1 instead of 0 IF not using var_names parameter.
        example: 'x_0 or x_1' - bad, 'x_1 or x_2' - good.
      format: str
    
    num_var: number of varaibles at string
      example: string = 'x_1 and x_2', num_var = 2
      format: int
    
    var_names: list of names of bool varaibles
      example: ['x_1', 'x_2', 'x_3', 'y_1', 'y_2', 'y_3']
      standard: []
      format: list(str)
      
  '''
  @staticmethod
  def get_bool_masks(num_vars):
    num_masks = 2 ** num_vars
    masks = []
    for number in range(0, num_masks):
      bin_mask = bin(number)[2:]
      bin_mask = (num_vars - len(bin_mask)) * '0' + bin_mask
      bin_mask = list(map(int, list(bin_mask)))
      bool_mask = list(map(bool, bin_mask))
      masks.append(bool_mask)
    return masks
  
  @staticmethod
  def parse_string(string, bool_mask, var_names=[]):
    if len(var_names) == 0:
      for i in range(1, len(bool_mask) + 1):
        string = re.sub(f'._{i}', str(bool_mask[i - 1]), string)
    else:
      for i, var_name in enumerate(var_names):
        string = string.replace(string, var_name, str(bool_mask[i]))
    return string

  @staticmethod
  def eval_string(string):
    return eval(string)
  
  @staticmethod
  def solve_string(string, num_var, var_names=[]):
    counter = 0
    bool_masks = BoolStringSolver.get_bool_masks(num_var)
    for mask in bool_masks:
      output = BoolStringSolver.eval_string(BoolStringSolver.parse_string(string, mask, var_names))
      if output == True:
        counter += 1
    return counter