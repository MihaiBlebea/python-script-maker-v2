#!/usr/bin/env python3

def main(config_path: str = None):
    if config_path is None:
        config_path = "config.yaml"

    with open(config_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            
            if "helpers" not in config:
                print("Could not find helpers key in config")
                return

            helpers = config["helpers"]

            if isinstance(helpers, list):
                print("Helpers key should be a list")
                return

            for helper in helpers:
                if helper == "api":
                    import api_helper
                    api_helper.main()

                if helper == "scrape":
                    import scrape_helper
                    scrape_helper.main()

        except yaml.YAMLError as err:
            print(f"Encountered error: {err}")


if __name__ == "__main__":
    main()