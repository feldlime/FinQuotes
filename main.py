from argparse import ArgumentParser

from aiohttp import web

from project import create_app, settings


def main() -> None:
    arg_parser = ArgumentParser(
        prog='python main.py',
        description='Detection development server',
    )
    arg_parser.add_argument(
        '--host',
        dest='host',
        help='TCP/IP hostname to serve on (default: %(default)r)',
        default=settings.HOST,
    )
    arg_parser.add_argument(
        '--port',
        dest='port',
        help='TCP/IP port to serve on (default: %(default)r)',
        default=settings.PORT,
    )
    args = arg_parser.parse_args()

    app = create_app()

    web.run_app(app, host=args.host, port=args.port)

    arg_parser.exit()


if __name__ == '__main__':
    main()
