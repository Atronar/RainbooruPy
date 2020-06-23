import math

def wilson_score(upvotes, downvotes):
    # Population size
    n = (upvotes + downvotes) / 1
    if n==0:
       return 0

    # Success proportion
    p_hat = upvotes / n

    # z and z^2 values for CI upper 99.5%
    z = 2.57583
    z2 = 6.634900189

    return (p_hat + z2/(2*n) - z * math.sqrt((p_hat*(1-p_hat)+z2/(4*n))/n))/(1+z2/n)

def set_limit(limit):

  if limit is not None:
    l = int(limit)
  else:
    l = None

  return l

def tags(q):
  if isinstance(q, str):
    q = q.split(',')
  tags = {str(tag).strip() for tag in q if tag}

  return tags if tags else set()

def join_params(old_params, new_params):
  new_dict = {**old_params, **new_params}

  return new_dict

def format_params(params):
  p = {}

  for key, value in params.items():
    if key == "search":
      if isinstance(value,str):
         p["search"] = value
      else:
         p["search"] = ",".join(value)
    elif key == "page":
      p["page"] = value if value>=0 else 0
    elif value:
      p[key] = value

  return p