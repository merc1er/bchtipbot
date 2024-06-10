import subprocess


def main():
    # Run tests with coverage
    subprocess.call(["python", "-m", "coverage", "run", "-m", "unittest", "discover"])

    # Generate the coverage report in the terminal
    subprocess.call(["python", "-m", "coverage", "report", "-m"])

    # Generate the HTML coverage report
    subprocess.call(["python", "-m", "coverage", "html"])

    print("\n\nTests completed.")
    print("HTML report generated at 'htmlcov/index.html'")


if __name__ == "__main__":
    main()
