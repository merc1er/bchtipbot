import subprocess


def main():
    subprocess.call(['python', '-m', 'unittest', 'tests.test_checks'])
    print('\n\nTests completed.')


if __name__ == '__main__':
    main()
