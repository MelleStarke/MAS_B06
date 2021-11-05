import pandas as pd
import numpy as np

def perform_TOPSIS(df, supplier_names):
    score = []
    nn = []
    pp = []

    # Hard-coded weights and impact for now.
    # weights = [0.2125, 0.1802, 0.0868, 0.1048, 0.0462, 0.0745, 0.0389, 0.0722, 0.0518, 0.0411, 0.0562, 0.035]
    a = pd.read_csv("../agents/util/q.csv", index_col="Unnamed: 0")
    impact = ['pos', 'pos', 'pos', 'pos', 'pos', 'pos', 'pos', 'pos', 'neg', 'neg', 'pos', 'pos']

    # Now we Calculate the Normalized Matrix and weighted Normalize matrix
    cols = len(df.columns)
    # making a copy of dataframe to use it later
    temp_df = df.copy()
    temp_df.iloc[:, 1:] = temp_df[temp_df.columns[1:]].astype(float)
    # Normalizing the supplier data
    b = temp_df.iloc[:, 1:].to_numpy()
    norm = np.linalg.norm(b)
    b = b / norm
    temp_df.iloc[:, 1:] = b
    # Normalizing the comparision matrix
    a = a.to_numpy()
    norm = np.linalg.norm(a)
    norm_a = a / norm
    # Construct the weighted normalized decision matrix by
    # multiplying the normalized decision matrix by its
    # associated weights.
    norm_weight_mat = np.matmul(b, norm_a)
    temp_df.iloc[:, 1:] = norm_weight_mat

    # # After creating a normalised matrix, We then multiply each value in a column with the corresponding weight given.
    # for i in range(1, cols):
    #     temp = 0
    #     for j in range(len(temp_df)):
    #         temp = temp + temp_df.iloc[j, i] ** 2
    #         temp = temp ** 0.5
    #     for j in range(len(temp_df)):
    #         temp_df.iat[j, i] = (temp_df.iloc[j, i] / temp) * weights[i - 1]

    # Now we calculate Ideal Best and Ideal worst and Euclidean distance for each row from ideal worst and ideal best value
    # Here we need to see the impact, i.e. is it ‘positive’ or ‘negative‘ impact.
    p_sln = (temp_df.max().values)[1:]
    n_sln = (temp_df.min().values)[1:]
    for i in range(1, cols):
        if impact[i - 1] == 'neg':
            p_sln[i - 1], n_sln[i - 1] = n_sln[i - 1], p_sln[i - 1]

    # now we calculate the distances and topsis scores now

    for i in range(len(temp_df)):
        temp_p, temp_n = 0, 0
        for j in range(1, cols):
            temp_p = temp_p + (p_sln[j - 1] - temp_df.iloc[i, j]) ** 2
            temp_n = temp_n + (n_sln[j - 1] - temp_df.iloc[i, j]) ** 2
        temp_p, temp_n = temp_p * 0.5, temp_n * 0.5
        score.append(temp_n / (temp_p + temp_n))
        nn.append(temp_n)
        pp.append(temp_p)

    # now we append the created lists into the original dataframe to rank it
    df['distance positive'] = pp
    df['distance negative'] = nn
    df['Topsis Score'] = score

    df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
    df = df.astype({"Rank": int})
    rankings = df["Rank"].to_dict()
    rankings = {name: rank for (name, rank) in zip(supplier_names, rankings.values())}
    sorted_rankings = [rankings[k] for k in sorted(rankings)]
    return sorted_rankings
    

def order_perms(D, Ns):
  """
  Computes the permutations of the order allocations.
  i.e. every way to distribute the order across the suppliers.
  
  D: demand, i.e. the order.
  Ns: nr. of suppliers.
  """
  
  def div_perms(n, r, ans=None):
    """
    Recursively calculates the permutations of one product order over the suppliers.

    n: amount of the product.
    r: nr. of suppliers (i.e. range)
    ans: result of the function
    """
    if ans is None:
      ans = [[0 for x in range(r)]]
      
    if n == 0:
      return ans
    
    new_ans = list()
    for a in ans:
      for ri in range(r):
        new_ans.append([ x+1 if i == ri else x for (i, x) in enumerate(a)])
    
    return div_perms(n-1, r, new_ans)
  
  
  def comb_perms(div_perms, ans=None):
    """
    Computes the permutations of the results of div_perms, resulting in every legal order division.
    
    div_perms: list of div_perms result for all products.
    ans: result of the function.
    """

    if len(div_perms) == 0:
      return ans
    
    if ans is None:
      #print(div_perms)
      dp = div_perms.pop(0)
      return comb_perms(div_perms, [[x] for x in dp])
    
    dp = div_perms.pop(0)
    new_ans = [ [] for  x in range(len(ans) * len(dp))]
    
    i = 0
    for a in ans:
      for p in dp:
        x = a + [p]
        new_ans[i] = x
        i += 1
    
    return comb_perms(div_perms, new_ans)
    
    
  div_ps = [div_perms(d, Ns) for d in D]

  return(comb_perms(div_ps))








