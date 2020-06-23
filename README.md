### Example

```python
from rainbooru import Search

for image in Search():
  id_number, score, tags = image.id, image.score, ", ".join(image.tags)
  print(f"#{id_number} - score: {score:>3} - {tags}")

for image in Search().query("safe", "princess luna"):
  print(image.full)
```