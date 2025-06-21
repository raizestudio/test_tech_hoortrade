import pytest
from colorama import Fore, Style
from django.core.management import call_command


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        if result.passed:
            print(Fore.GREEN + "PASSED: " + item.name + Style.RESET_ALL)
        elif result.failed:
            print(Fore.RED + "FAILED: " + item.name + Style.RESET_ALL)
        elif result.skipped:
            print(Fore.YELLOW + "SKIPPED: " + item.name + Style.RESET_ALL)


@pytest.fixture(autouse=True)
def load_fixtures(db):
    print(Fore.CYAN + "Loading fixtures..." + Style.RESET_ALL)
    call_command("loaddata", "dev/genre.json")
