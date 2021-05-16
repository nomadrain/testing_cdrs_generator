#!/usr/bin/env python
import string
import random
from time import time
from simplemsisdn import SimpleMSISDN
from ua_ndc import landline_ndc, mobile_ndc


class FakeMsisdnGenerator():
    """
    Configurable generator of fake MSISDNs

    Produces a regular fake MSISDN:
    e.g.
    +000-11-3939391
    ^
    Country code, 2 or 3 digits
         ^
         National destination code also known as operator code
            ^
            Personal number
    :param allowed_country_codes - Iterable of strings
    :param allowed_national_destination_codes - Iterable of strings
    :param subscriber_number_length - scalar int
    :param preferable_ndc - National destination code which will be selected with the probability given
        in the preferable_prob parameter
    :param preferable_prob. Int. Probability of choosing the preferable_ndc as an NDC for the generated MSISDN
    """

    def __init__(self,
                 allowed_country_codes=('+000', '+111'),
                 allowed_national_destination_codes=('11', '22', '33'),
                 subscriber_number_length=7,
                 preferable_ndc='50',
                 preferable_prob=80
                 ):
        if allowed_country_codes:
            self.allowed_country_codes = allowed_country_codes
        else:
            self.allowed_country_codes = ('000', '111')

        if allowed_national_destination_codes:
            self.allowed_national_destination_codes = allowed_national_destination_codes
        else:
            self.allowed_national_destination_codes = ('11', '22', '33')

        if subscriber_number_length and type(subscriber_number_length) is int:
            self.subscriber_number_length = subscriber_number_length
        else:
            self.subscriber_number_length = 7

        if preferable_ndc:
            self.preferable_ndc = preferable_ndc
        else:
            self.preferable_ndc = '50'

        if preferable_prob and type(preferable_prob) is int:
            self.preferable_prob = int(preferable_prob)
        else:
            self.preferable_prob = 80

    def get(self):
        """
        :return: Instance of SimpleMSISDN with a country code and a national destination code randomly selected from
        the given params and randomly generated subscriber number of the given length
        """
        random.seed(time())
        cc = random.choice(self.allowed_country_codes)
        ndc = random.choices((self.preferable_ndc, random.choice(self.allowed_national_destination_codes)),
                             weights=(self.preferable_prob, 100 - self.preferable_prob), k=1)[0]
        sn = ''.join(random.choices(string.digits, k=self.subscriber_number_length))
        return SimpleMSISDN(country_code=cc, national_destination_code=ndc, subscriber_number=sn)


if __name__ == '__main__':
    anumber = FakeMsisdnGenerator(allowed_country_codes=('999',),
                                  allowed_national_destination_codes=mobile_ndc,
                                  subscriber_number_length=7,
                                  preferable_ndc='50')
    for numcount in range(10):
        print(str(anumber.get()))

    print()

    for numcount in range(10):
        print(repr(anumber.get()))

