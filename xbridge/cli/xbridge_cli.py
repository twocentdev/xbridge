import argparse
import logging
import sys
from logging import Logger

from others.app_config import AppConfig
from services.instance_parser_service_handler import \
    InstanceParserServiceHandler
from services.taxonomy_loader_service_handler import \
    TaxonomyLoaderServiceHandler

logger = logging.getLogger(__name__)


class XBridgeCLI:

    __modes = ["tax", "inst"]

    def is_mode_valid(self, mode: str) -> bool:
        return mode in self.__modes

    def main(self):
        parser = argparse.ArgumentParser(
            prog="EBA-XBridge",
            description=""
        )
        parser.add_argument("-c", "--config")
        parser.add_argument("mode")
        parser.add_argument("-f", "--filter", action="append")
        parser.add_argument("-i", "--inst")
        parser.add_argument("-m", "--mods")
        parser.add_argument("-o", "--output")
        parser.add_argument("--overwrite", action="store_true")
        parser.add_argument("-t", "--tax")
        parser.add_argument("--verbose", action="store_true")
        args = parser.parse_args(sys.argv)

        if args.verbose:
            Logger.setLevel(logger, logging.DEBUG)
        else:
            Logger.setLevel(logger, logging.INFO)
        logger.debug("Verbose mode enabled")

        # Load AppConfig
        if args.config:
            try:
                AppConfig.load_config(args.config)
            except Exception:
                logger.fatal("An error occurred while loading AppConfig.")
                return -1

        if not self.is_mode_valid(args.mode):
            logger.fatal("Invalid mode. Please read help for more information.")
            return -1

        if args.mode == "tax":
            logger.debug("About to call Taxonomy loader service")
            TaxonomyLoaderServiceHandler.load(
                tax_path=args.tax,
                modules_path=args.mods,
                overwrite=args.overwrite,
                filters=args.filter
            )
        else:
            logger.debug("About to call Instance parser service")
            InstanceParserServiceHandler.parse(
                inst_path=args.inst,
                modules_path=args.mods,
                output_path=args.output
            )
        return 0

if __name__ == "__main__":
    app = XBridgeCLI()
    sys.exit(app.main())
