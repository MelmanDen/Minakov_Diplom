import os
import subprocess


async def run_tests():
    tests_dir = 'tests'
    test_files = [f for f in os.listdir(tests_dir) if not f.startswith('__') and f.endswith('.py')]

    for test_file in test_files:
        test_path = os.path.join(tests_dir, test_file)

        command = f'pytest {test_path}'

        subprocess.Popen(['start', 'cmd', '/k', command], shell=True)
