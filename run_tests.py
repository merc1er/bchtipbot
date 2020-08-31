import subprocess


def main():
    subprocess.call(["python", "-m", "unittest"])
    print("\n\nTests completed.")


if __name__ == "__main__":
    main()
