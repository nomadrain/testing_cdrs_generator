import uuid
import time
import datetime
import random
from fake_msisdn_generator import FakeMsisdnGenerator
from ua_ndc import mobile_ndc

# The header defines names of the CDR fields, used for import to the external generators
header = 'RECORD_ID,CALLING_MSISDN,CALLED_MSISDN,START_TIME,END_TIME,DURATION,' \
         'CALL_TYPE,CHARGING_TYPE,CHARGE,CALL_RESULT'

# This is a national destination code of operator which is assumed to be the owner of the current radio network
# This value affects the ammount charged
native_ndc = '50'

# Generators for the calling and called numbers, here we assume that ingress and egress calls can
# sometimes come from any mobile operator
egress_gn = FakeMsisdnGenerator(allowed_country_codes=('380',),
                                allowed_national_destination_codes=mobile_ndc,
                                subscriber_number_length=7,
                                preferable_ndc=native_ndc,
                                preferable_prob=95)

ingress_gn = FakeMsisdnGenerator(allowed_country_codes=('380',),
                                 allowed_national_destination_codes=mobile_ndc,
                                 subscriber_number_length=7,
                                 preferable_ndc=native_ndc,
                                 preferable_prob=50)


class FakeCallDetailRecord():

    def __init__(self, unix_timestamp=None, seconds_length=0):
        """

        :param unix_timestamp: int. Timestamp of the call start.
        :param seconds_length: int. Length of the call. If negative negative is provided it is converted
            to the positive number. Default = 0
        """
        if not unix_timestamp or not type(int(unix_timestamp)) is int:
            raise ValueError('The unix_timestamp for the CDR should be provided as a valid integer or string integer. '
                             'representation. 0 is not acceptable '
                             )

        if not type(int(unix_timestamp)) is int:
            raise ValueError('The seconds_length should be provided as an integer.')

        self.seconds_length = abs(seconds_length)

        ts = str(unix_timestamp)
        tsend = str(int(unix_timestamp) + seconds_length)

        fmt = "%Y-%m-%dT%H:%M:%S"
        self.id = f'{uuid.uuid1()}-{time.time()}'
        egress = egress_gn.get()
        ingress = ingress_gn.get()
        self.calling_msisdn = repr(egress)
        self.called_msisdn = repr(ingress)
        self.start_time = datetime.datetime.fromtimestamp(int(ts)).strftime(fmt)
        self.end_time = datetime.datetime.fromtimestamp(int(tsend)).strftime(fmt)
        # self.call_type = random.choice((1, 2, 3, 4, 5, 6, 7))
        # self.call_type = random.choice(['VOICE', 'SMS'])
        self.call_type = 'VOICE'

        # Charging policy generation
        # Assuming that the network owner has NDC code equal to native_ndc e.g. '50'
        # Then if both ingress and egress MSISDNs has NDC == native_ndc the charge is 0
        # Otherwise if one of the MSISDNs has native NDC and another has anything else the charge
        #   is random.random/2 per minute
        # Otherwise if both ingress and egress MSISDNs are aliens the charge is random.random * 9 per minute
        if egress.get_ndc() == ingress.get_ndc() and egress.get_ndc() == native_ndc:
            self.charge = 0
            self.charging_type = 1
        elif egress.get_ndc() == native_ndc or ingress.get_ndc() == native_ndc:
            self.charge = random.random() / 2 * seconds_length / 60
            self.charging_type = 2
        else:
            self.charge = random.random() * 9 * seconds_length / 60
            self.charging_type = 3

    def __str__(self):
        cdr = f''
        cdr += f'{self.id},'
        cdr += f'{self.calling_msisdn},'
        cdr += f'{self.called_msisdn},'
        cdr += f'{self.start_time},'
        cdr += f'{self.end_time},'
        cdr += f'{self.seconds_length},'
        cdr += f'{self.call_type},'
        cdr += f'{self.charging_type},'
        cdr += f'{round(self.charge, 2)},'

        if self.seconds_length == 0:
            cdr += f'{random.choices(("BUSY", "UNREACHABLE", "NETWORK_ERROR"), weights=[90, 9, 1], k=1)[0]}'
        else:
            cdr += f'ANSWERED'

        return cdr

    def get(self):
        return str(self)
        

if __name__ == '__main__':
    print(FakeCallDetailRecord(unix_timestamp=1, seconds_length=15))
