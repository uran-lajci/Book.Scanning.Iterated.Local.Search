import glob
import os
from concurrent.futures import ProcessPoolExecutor

from models import Parser
from models import Solver

INPUT_INSTANCES_DIR = 'input'
OUTPUT_INSTANCES_DIR = 'output'

MINUTES_TO_RUN = 10
MAX_ITERATIONS = 1000
NUM_CORES = 40


def run_solver(version: str, instance_path: str) -> None:
    output_sub_dir = os.path.join(OUTPUT_INSTANCES_DIR, version)
    os.makedirs(output_sub_dir, exist_ok=True)

    solver = Solver()
    parser = Parser(instance_path)
    data = parser.parse()

    result = solver.iterated_local_search(
        data,
        time_limit=MINUTES_TO_RUN * 60,
        max_iterations=MAX_ITERATIONS
    )
    score = result.fitness_score
    instance_name = os.path.basename(instance_path)
    print(instance_name, score, f'version: {version}')

    output_file = os.path.join(output_sub_dir, instance_name)
    result.export(output_file)


def main():
    instance_paths = glob.glob(f'{INPUT_INSTANCES_DIR}/*.txt')
    jobs = []

    for v in range(1, 6):
        version = f'v{v}'
        for path in instance_paths:
            jobs.append((version, path))

    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        futures = [executor.submit(run_solver, version, path) for version, path in jobs]

        for future in futures:
            future.result()  


if __name__ == '__main__':
    main()
