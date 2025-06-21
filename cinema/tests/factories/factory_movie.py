import random

import factory
from faker import Faker

from cinema.models import Movie, MovieStatus
from core.models import DataSource

fake = Faker()


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.LazyAttribute(lambda x: fake.sentence(nb_words=3))
    original_title = factory.LazyAttribute(lambda x: fake.sentence(nb_words=3))
    original_language = factory.LazyAttribute(lambda x: fake.language_code())
    description = factory.LazyAttribute(lambda x: fake.paragraph(nb_sentences=5))
    release_date = factory.LazyAttribute(lambda x: fake.date_between(start_date="-30y", end_date="today"))
    status = factory.LazyAttribute(lambda x: random.choice([choice[0] for choice in MovieStatus.choices()]))
    adult_content = factory.LazyAttribute(lambda x: fake.boolean())
    source = factory.LazyAttribute(lambda x: random.choice([ds.name for ds in DataSource]))
