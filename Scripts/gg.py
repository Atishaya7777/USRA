from visualize import Point, PointConfiguration


def check():
    config = PointConfiguration(10, {1, 2})
    success = config.generate_config()
    if success:
        print("Configuration generated successfully.")
        print(config.configurations)
    else:
        print("Failed to generate configuration.")
        print(config.configurations)


if __name__ == "__main__":
    check()
