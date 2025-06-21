import argparse
import glob
import os

from models import Parser
from models import Solver

INPUT_INSTANCES_DIR = 'input'
OUTPUT_INSTANCES_DIR = 'output'

MINUTES_TO_RUN = 10

def main(version: str) -> None:
    output_sub_dir = os.path.join(OUTPUT_INSTANCES_DIR, version)
    os.makedirs(output_sub_dir, exist_ok=True)

    solver = Solver()

    instance_paths = glob.glob(f'{INPUT_INSTANCES_DIR}/*.txt')

    for instance_path in instance_paths:
        parser = Parser(instance_path)
        data = parser.parse()
        result = solver.iterated_local_search(data, 
                                              time_limit=MINUTES_TO_RUN * 60, 
                                              max_iterations=1000)
        score = result.fitness_score
        instance_name = os.path.basename(instance_path)
        print(instance_name, score, f'version: {version}')
        output_file = os.path.join(output_sub_dir, instance_name)
        result.export(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', type=str, required=True)

    args = parser.parse_args()
    main(args.version)
