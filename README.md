# Data Anonymizer

This application anonymize personal sensitive data in csv file.

The source code sits in [github](https://github.com/yorkhuang-au/anonymizer)

## Assumptions and Limitations
Some assumptions and limitations are made as below.

### Source CSV file
The csv file must be well formatted. The code will fail if the csv file can't be read properly.

The first line is headers with 4 columns: first_name,last_name,address,date_of_birth.
Fields are delimited by commas and quoted or escapped if commas or quote are in the data fields.

Sample input csv file is below.

app/data/sample_input.csv
```
first_name,last_name,address,date_of_birth
York, Huang, 1 martin st sydney NSW 2023,2001-01-24
David,Jones, 12 George st Kensington NSW 2001,1971-07-05
Han,Lee," 43 belmore road Doncaster, VIC 3433",1980-10-12
Jessica,Smiths,"12/23 Railway st, Melbourne, VIC 3001",2002-11-21
```

### Anonymizing Algorithms
Python package faker is used to anonymize data. It is in [PyPi here](https://pypi.org/project/Faker/).

The code creates names and addresses like normal Australian names and addresses.

The code maintains idempotency, e.g. it creates the same anonymized data given the same source data. This is achived by setting the same seed for Faker for each faker call. The seed is constructed by joining a secret string and the original data which is stripped leading and trailing spaces and is converted to upper case. The secret is used to hide the actual seed sent to Faker.

Given the space of names and addresses are limitted, Faker could return the same data as the original data. In the tests, an error rate of 5% is allowed for first names and last names, 1% is allowed for addresses, and 0.5% is allowed for the combination of (first_name, last_name, address).


## How to build

Make sure docker engine or docker desktop is installed and running.

### Get the source code
The source code is in [github](https://github.com/yorkhuang-au/anonymizer)

```
cd ~
git clone git@github.com:yorkhuang-au/anonymizer.git
cd ~/anonymizer
```

### Unit Test
Docker stages are used for testing and production.

For unit test
```
cd ~/anonymizer/app
docker build . -t test -f Dockerfile --target test --progress=plain --no-cache
```

### Build prod image
```
cd ~/anonymizer/app
docker build . -t prod -f Dockerfile --target prod
```

### Run the container

#### Use your own secret and file
First, create the input file in the ~/anonymizer/app/data folder.
An sample input file is provided.

```
ls ~/anonymizer/app/data/sample.csv
```

Run the container on the input file.
```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod <secret> /data/<input filename> /data/<output filename>
```

For example, 

```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod A$!23 /data/sample.csv /data/out_sample.csv
```
The output file will be created at ~/anonymizer/app/data folder.

### Use your own secret, auto-generate file
```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod <secret>
```

For example, 

```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod A$!23
```

It will create a input file like '~/anonymizer/app/data/input_yyyyMMdd_HHMMSS.csv'.
The output file is '~/anonymizer/app/data/out_input_yyyyMMdd_HHMMSS.csv'.


### Auto-generate file and secret
```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod
```

For example, 

```
cd ~/anonymizer/app
docker run --rm -v $(pwd)/data:/data prod
```

It will create a input file like '~/anonymizer/app/data/input_yyyyMMdd_HHMMSS.csv'.
The output file is '~/anonymizer/app/data/out_input_yyyyMMdd_HHMMSS.csv'.
