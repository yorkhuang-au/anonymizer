import pytest
import pandas as pd
from anonymizer import anonymizer as ano
from faker import Faker


# Number of records to test. This value needs to be big enough to 
# ensure error_rate is acceptable.
TEST_SIZE = 1000


@pytest.fixture
def fake():
    """
    Faker to mock test data.
    """
    return Faker(['en-AU'])


@pytest.fixture
def secret():
    return "A!Ob3#"


@pytest.fixture
def first_names(fake):
    return [fake.first_name() for _ in range(TEST_SIZE)]


@pytest.fixture
def last_names(fake):
    return [fake.last_name() for _ in range(TEST_SIZE)]


@pytest.fixture
def addresses(fake):
    return [fake.address() for _ in range(TEST_SIZE)]


@pytest.fixture
def original_data(fake, first_names, last_names, addresses):
    date_of_births = [fake.date() for _ in range(TEST_SIZE)]
    return pd.DataFrame(zip(first_names, last_names, addresses, date_of_births), 
                        columns=['first_name', 'last_name', 'address', 'date_of_birth'])


def check_results(secret: str, originals: list, anonymize_func, error_rate=0) -> None:
    anonymizeds1 = [anonymize_func(secret, n) for n in originals]
    anonymizeds2 = [anonymize_func(secret, n) for n in originals]

    # error is True if original == anonymized, False otherwise.
    org_ano1_errs = [o==a for o, a in zip(originals, anonymizeds1)]

    # error is True if anonymized 1st time != anonymized 2nd time
    ano1_ano2_errs = [a1!=a2 for a1, a2 in zip(anonymizeds1, anonymizeds2)]

    print(originals)
    print(anonymizeds1)
    print(anonymizeds2)
    print(sum(org_ano1_errs))

    # Since fake creates random value, the random value could be the same as the original value.
    # If the error rate is less than error_rate, it is acceptable. -- My assumption.
    assert sum(org_ano1_errs) < len(originals) * error_rate, \
        f"Not less than {100 - error_rate*100}% of the anonymized values must be different from the original values."

    # This is to test the idempotency.
    assert sum(ano1_ano2_errs) == 0, \
        "The 1st time anonymized value should be the same as the 2nd time anonymized value."


def test_anonymize_first_name(first_names, secret):
    # Accept if error rate is less than 5%, eg. 5% of the anonymized first names are the same
    # as original first names due to the random values of names are limitted.
    check_results(secret, first_names, ano.anonymize_first_name, 0.05)


def test_anonymize_last_name(last_names, secret):
    # Accept if error rate is less than 5%, eg. 5% of the anonymized last names are the same
    # as original last names due to the random values of names are limitted.
    check_results(secret, last_names, ano.anonymize_last_name, 0.05)


def test_anonymize_address(addresses, secret):
    # Accept if error rate is less than 1%, eg. 1% of the anonymized addresses are the same
    # as original addresses due to the random values of addresses are limitted.
    check_results(secret, addresses, ano.anonymize_address, 0.01)


def test_anonymize_data(secret: str, original_data: pd.DataFrame):
    anonymized_data = ano.anonymize_data(secret, original_data.copy(True))

    print(original_data)
    print(anonymized_data)

    assert len(anonymized_data) == len(original_data), "Anonymized data should be the same size of original data."
    assert sum(original_data['date_of_birth'] != anonymized_data['date_of_birth']) == 0, "date_of_birth column should not change."
    
    first_name_errs = original_data['first_name'] == anonymized_data['first_name']
    assert sum(first_name_errs) < 0.05 * len(original_data.index), \
        "No more than 5% of anonymized first names are the same as original data."

    last_name_errs = original_data['last_name'] == anonymized_data['last_name']
    assert sum(last_name_errs) < 0.05 * len(original_data.index), \
        "No more than 5% of anonymized last names are the same as original data."
    
    address_errs = original_data['address'] == anonymized_data['address']
    assert sum(address_errs) < 0.01 * len(original_data.index), \
        "No more than 1% of anonymized addresses are the same as original data."
    
    row_errs = [f and l and a for f, l, a in zip(first_name_errs, last_name_errs, address_errs)]
    print(sum(row_errs))
    assert sum(row_errs) < 0.005 * len(original_data.index), \
        "No more than 0.5% of anonymized rows are the same as original data."
