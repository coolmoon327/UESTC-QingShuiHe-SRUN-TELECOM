import platform
import logging

logger = logging.getLogger(__name__)


def get_platform() -> str:
    system = platform.system()
    arch = platform.architecture()
    machine = platform.machine()

    logger.debug(f"System: {system}")
    logger.debug(f"Architecture: {arch}")

    platform_both = "unknown"

    # see https://en.wikipedia.org/wiki/Uname
    match system:
        case "Windows":
            match arch[0]:
                case "64bit":
                    platform_both = "win64"
                case "32bit":
                    platform_both = "win32"
        case "Darwin":
            match machine:
                case "arm64":  # what `uname -m`` returns on Big Sur and Monterey
                    platform_both = "mac-arm64"
                # case "AMD64":
                #     platform_both = "mac-x64"
                # not for macos
                case "x86_64":
                    platform_both = "mac-x64"
        case "Linux":
            match arch[0]:
                case "64bit":
                    platform_both = "linux64"
        case _:
            logger.error(
                "Unsupported Platform: "
                + "\t".join([system, arch[0], arch[1], machine])
            )

    return platform_both
