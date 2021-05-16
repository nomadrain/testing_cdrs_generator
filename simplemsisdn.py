class IncorrectMsisdnData(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class SimpleMSISDN(object):

    def __init__(self,
                 country_code=None,
                 national_destination_code=None,
                 subscriber_number=None):
        """
        Instance of a regular MSISDN also known as a TN or Full Telephone Number:
        e.g.
        +000-11-3939391
        ^
        Country code, 2 or 3 digits
             ^
             National destination code also known as operator code
                ^
                Personal number

        repr(SimpleMSISDN instance) will produce a plane string containing only digits contrary to
            str(SimpleMSISDN instance) formatted as +{country_code}-{national_destination_code}-{subscriber_number}

        :param country_code: String. The country code as a first part of MSISDN e.g. 380 (Ukraine). Accepts any value,
            no validation
        :param national_destination_code: String. Landlined code (e.g. 44  Kyiv, Ukraine) or an operator code
            (e.g. 93 Lifecell, Ukraine), no validation applied
        :param subscriber_number: several digits personal subscriber number
        :raises IncorrectMsisdnData if any of the params is None or empty

        Attributes:

        number_class: Commercial class of the Subscriber Number e.g. 'GOLDEN', 'SILVER', 'BRONZE', 'REGULAR'

        """

        if not country_code or not national_destination_code or not subscriber_number:
            raise IncorrectMsisdnData("Some MSISDN components are absent from the constructor's parameters")

        self.__country_code = str(country_code)
        self.__national_destination_code = str(national_destination_code)
        self.__subscriber_number = str(subscriber_number)

        # This is to be defined as GOLDEN, SILVER etc.
        self.number_class = self.__detect_number_class()

    def __detect_number_class(self):
        # TODO: add check_gold, check_silver, check_bronze, check_super
        return 'REGULAR'

    def __repr__(self):
        return f'{self.__country_code}{self.__national_destination_code}{self.__subscriber_number}'

    def __str__(self):
        return f'+{self.__country_code}-{self.__national_destination_code}-{self.__subscriber_number}'

    def __hash__(self):
        return hash((self.__country_code,
                     self.__national_destination_code,
                     self.__subscriber_number))

    def get_local_only(self, leading_zero=False):
        """
        :param: leading_zero, bool. If True adds 0 to the beginning of the local representation
        :return: MSISDN as a string of digits without country code
        """
        zero = '0' if leading_zero else ''
        return f'{zero}{self.__national_destination_code}{self.__subscriber_number}'

    def get_ndc(self):
        """

        :return: the NDC code
        """
        return self.__national_destination_code


if __name__ == '__main__':
    a = SimpleMSISDN(380, 22, 33)
# TODO: add verifications for the components, use the existing phonenumber lib? add link to the phonenumber repo
