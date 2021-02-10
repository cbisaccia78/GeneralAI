from pathlib import Path


skeles = Path('./skeletons')
line_count = 0
for file in skeles.glob('**/*.py'):
    with open(file) as f:
        while f.readline():
            line_count += 1
print(line_count)



