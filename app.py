from models import Parser
from models import Solver
import os


solver = Solver()
directory = os.listdir('input')

print("---------- ITERATED LOCAL SEARCH WITH RANDOM RESTARTS ----------")
for file in directory:
    if file.endswith('.txt'):
        parser = Parser(f'./input/{file}')
        data = parser.parse()
        result = solver.iterated_local_search(data, time_limit=300, max_iterations=1000)
        print(f"Final score for {file}: {result[0]:,}")
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, file)
        result[1].export(output_file)
        print("----------------------")


