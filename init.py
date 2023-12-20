import os
import requests
import argparse

url_pattern = 'https://adventofcode.com/2023/day/{}/input'
code_template = '''input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = f.readlines()

def part_one():
    return None

print(f'Part One: {part_one()}')

def part_two():
    return None

print(f'Part Two: {part_two()}')
'''

def init(day, aoc_session):
    url = url_pattern.format(day)
    response = requests.get(url, cookies={'session': aoc_session})
    if response.status_code != 200:
        print("Failed to download the file:", response.status_code, response.text)
        return
    
    file_folder = f'day{day}'
    input_file = 'input.txt'
    solution_file = 'solution.py'
    os.mkdir(file_folder)
    with open(f'{file_folder}/{input_file}', 'w') as f:
        f.write(response.text)
    with open(f'{file_folder}/{solution_file}', 'w') as f:
        f.write(code_template)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize a new day.')
    parser.add_argument('day', help='The day to initialize.')
    parser.add_argument('session_token', help='The session token for Advent of Code.')
    args = parser.parse_args()

    init(args.day, args.session_token)