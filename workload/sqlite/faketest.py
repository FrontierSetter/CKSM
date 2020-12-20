from faker import Faker
fake = Faker()
fake.seed_instance(4321)

for i in range(10):
    print(fake.name())

for i in range(10):
    print(fake.name())

fake.seed_instance(4321)

for i in range(10):
    print(fake.name())

for i in range(10):
    print(fake.name())