from models import Parser
from models import Solver
from multiple_validator import validate_all_solutions
import os


solver = Solver()
directory = os.listdir('input')
results = []
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

print("---------- ITERATED LOCAL SEARCH WITH RANDOM RESTARTS ----------")
for file in directory:
    if file.endswith('.txt'):
        parser = Parser(f'./input/{file}')
        data = parser.parse()
        result = solver.iterated_local_search(data, time_limit=300, max_iterations=1000)
        score = result.fitness_score
        results.append((file, score))
        print(f"Final score for {file}: {score:,}")
        output_file = os.path.join(output_dir, file)
        result.export(output_file)
        print("----------------------")



print("\nValidating all solutions...")
validate_all_solutions(input_dir='input', output_dir=output_dir)

# Print summary of all instances
print("\nSummary of all instances:")
print("-" * 50)
print(f"{'Instance':<20} {'Score':>15}")
print("-" * 50)
for file, score in results:
    print(f"{file:<20} {score:>15,}")
print("-" * 50)

# Write summary to a text file
summary_file = os.path.join(output_dir, 'summary_results.txt')
with open(summary_file, 'w') as f:
    f.write("Summary of all instances:\n")
    f.write("-" * 50 + "\n")
    f.write(f"{'Instance':<20} {'Score':>15}\n")
    f.write("-" * 50 + "\n")
    for file, score in results:
        f.write(f"{file:<20} {score:>15,}\n")
    f.write("-" * 50 + "\n")
print(f"\nSummary has been written to: {summary_file}")
