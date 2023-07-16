import argparse
import logging
import os

import mod_builder.builder

log_string_format = '%(asctime)s  [%(levelname)s]: %(message)s'


def main():
    """
    main entry point
    """
    parser = argparse.ArgumentParser(description="The app builds and registers registers a module in the os")
    parser.add_argument("-c", "--config", help="the config file for this program", type=str, default="")
    parser.add_argument("--verbose", '-v',
                        help="sets the app in debug mode",
                        action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=log_string_format)
    else:
        logging.basicConfig(level=logging.INFO, format=log_string_format)

    conf = mod_builder.builder.load_config(args.config)
    mod_builder.builder.build(conf)
    mod_builder.builder.install(conf)


if __name__ == '__main__':
    main()
