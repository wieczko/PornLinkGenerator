import argparse
from license_manager import generate_license


def main():
    parser = argparse.ArgumentParser(description="Generuje numer seryjny licencji dla programu PornLinkGenerator.")
    parser.add_argument("username", nargs="?", default="default-user", help="Nazwa użytkownika / właściciela licencji")
    parser.add_argument("--days", type=int, default=3650, help="Liczba dni ważności licencji (domyślnie 3650)")
    args = parser.parse_args()

    serial = generate_license(args.username, days=args.days)
    print("Serial:")
    print(serial)


if __name__ == "__main__":
    main()
