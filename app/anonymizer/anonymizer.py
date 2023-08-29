"""
This module is to anonymize a csv file.
"""

import sys
import os
import datetime
import pandas as pd
from faker import Faker


# This is the faker to anonymize data using AU locale.
fake = Faker(['en-AU'])


def usage():
    """
    Show usage
    """
    print("""
    Usage: python3 main.py <secret> <input filename> <output filename>
          secret: used to anonymize data.
          input filename: input original csv file
          output filename: output anonymized csv file
    """)


def read_data(filename: str) -> pd.DataFrame:
    """ 
    Read original data from a csv file into pandas dataframe.

    The csv must be well-formatted. It has 4 columns: first_name, last_name, address, date_of_birth.
    The 1st line is the header and contains the 4 column names.
    Each row contains data. If a field containing comma (,) or double-quote (") characters, enclose 
    the field in double-quotes.

    And example of the csv file is as below:
    
    first_name,last_name,address,date_of_birth
    David,Jone,1 George st Sydney NSW 2112,05/09/1991
    John,Lee,"32 Charles Road, Kingsford, NSW, 2008",23/11/1980

    In the returned dataframe, each column name's leading and trailing whitespace is removed. The 
    column names are converted to lowercase.

    :param filename: The name of the file
    :return: A pandas.DataFrame
    """
    try:
        df = pd.read_csv(filename, quotechar='"')
        df.columns = [c.strip().lower() for c in df.columns]
    except Exception as e:
        print("error in loading file: ", filename)
        print("error: ", e)
        usage()
        sys.exit(1)
    return df


def anonymize_first_name(secret: str, first_name: str) -> str:
    """
    Anonymize first name.

    Use Faker to create a random first name. In order to maintain the idempotency, create the same 
    seed for Faker. Concatenate a secret string and the upper case of the stripped first_name to 
    create the same seed for the same first_name. The secret is used to hide the actual seed.
    
    :param secret: The secret string to create seed for Faker
    :param first_name: The original first_name
    :return: The anonymized first name.
    """

    Faker.seed(f"{secret}{first_name.strip().upper()}")
    return fake.first_name()


def anonymize_last_name(secret: str, last_name: str) -> str:
    """
    Anonymize last name.

    Use Faker to create a random last name. In order to maintain the idempotency, create the same 
    seed for Faker. Concatenate a secret string and the upper case of the stripped last_name to 
    create the same seed for the same last_name. The secret is used to hide the actual seed.
    
    :param secret: The secret string to create seed for Faker
    :param last_name: The original last_name
    :return: The anonymized last name.
    """

    Faker.seed(f"{secret}{last_name.strip().upper()}")
    return fake.last_name()


def anonymize_address(secret: str, address: str) -> str:
    """
    Anonymize address.

    Use Faker to create a random address. In order to maintain the idempotency, create the same 
    seed for Faker. Concatenate a secret string and the upper case of the stripped address to 
    create the same seed for the same address. The secret is used to hide the actual seed.
    
    :param secret: The secret string to create seed for Faker
    :param address: The original address
    :return: The anonymized address.
    """    

    Faker.seed(f"{secret}{address.strip().upper()}")
    return fake.address().replace('\n', ' ')


def anonymize_data(secret: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Anonymize first_name, last_name and address columns in the input dataframe.

    :param secret: The secret string to create seed for Faker
    :param df: A pandas.DataFrame of the original data
    :return: The dataframe with anonymized data
    """

    df['first_name'] = list(map(anonymize_first_name, [secret]*len(df), df['first_name']))
    df['last_name'] = list(map(anonymize_last_name, [secret]*len(df), df['last_name']))
    df['address'] = list(map(anonymize_address, [secret]*len(df), df['address']))
    
    return df


def write_data(df: pd.DataFrame, filename: str) -> None:
    """
    Write output data to a csv file.

    :param df: The anonymized dataframe
    :param filename: The output csv filename
    """

    df.to_csv(filename, encoding='utf-8', index=False)


def anonymize_csv(secret: str, input_filename: str, output_filename: str) -> None:
    """
    Anonymize first_name, last_name, and address in the input csv file. Output the anonymized
    data back to the output csv file.

    :param secret: The secret string to create seed for Faker
    """

    original_df = read_data(input_filename)
    anonymized_df = anonymize_data(secret, original_df)
    write_data(anonymized_df, output_filename)


def generate_source_csv(record_count:int) -> str:
    """
    Generate the source csv file in /data folder.

    :param record_count: The number of records to generate in the csv file.
    :return: The csv filename generated.
    """
    filename = os.path.join("/data", f"input_{datetime.datetime.now().strftime('%y%m%d_%H%M%S')}.csv")
    first_names = [fake.first_name() for _ in range(record_count)]
    last_names = [fake.last_name() for _ in range(record_count)]
    addresses = [fake.address().replace('\n', '') for _ in range(record_count)]
    date_of_births = [fake.date() for _ in range(record_count)]

    df = pd.DataFrame(zip(first_names, last_names, addresses, date_of_births),
                      columns=['first_name', 'last_name', 'address', 'date_of_birth'])
    write_data(df, filename)
    return filename





