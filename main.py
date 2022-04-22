from timeit import timeit

from construct_profile_HMM_pseudocounts.construct_profile_HMM import profile_HMM_pseudocounts as f_HMM
from construct_profile_HMM_pseudocounts.construct_profile_HMM0 import profile_HMM_pseudocounts as n_HMM


def profile_HMM_pseudocounts(*args):
    number = 1000
    print(timeit(lambda: f_HMM(*args), number=number) / number)
    # print(timeit(lambda: n_HMM(*args), number=number) / number)


if __name__ == '__main__':
    # print(profile_HMM(0.25, 'ABCDE', ['BAB', 'D-D']))
    # print(profile_HMM(0.9391285067623935, 'ABCDE', ['BCAA', 'CCEC', 'CDA-', 'BBDE']))
    # print(profile_HMM(0.25, 'ABCDE',
    #                   ['E-DDB-ADAC', 'BCDEEC-ABC', 'ECB-EEEC-E', 'AACDECBBD-', 'EDD--CB-DD', 'CEAABDEEAA', 'EB-CBAECC-',
    #                    'B-B-DADAED', 'DCDE-DAEA-', 'CCB-CDBC-C', 'EBBDBABEAD', 'DB-BDABAE-', 'DEAB-EDCCB', 'DCBEBDEBBB',
    #                    'BB--EEDB--', 'CDCADD--ED', 'ADAEDE-DE-', 'AB-AEB-DCB']))
    # print(n_HMM(0.25, 0.04, 'ABCDE', ['ABD-DDB', 'CAACCEC']))
    # print(n_HMM(0.25, 0.09, 'ABCDE',
    #             ['CEBD-C-B-A', 'CCADAEEBAE', '-DDC-C-DCE', 'BABAACDBCA', 'BAEDCCE-CD', 'D--DC-BAAC', 'AEB-BA-A--',
    #              'BA-BE-EEA-', 'E-EC-AABED', 'ECEAB-C-BD']))
    # print(profile_HMM_pseudocounts(0.25519959248016066, 0.02, 'ABCDE',
    #                                ['-BBDE-BE', 'C-BCEBE-', 'BBBCCDDE', 'CBBACCEB']))
    profile_HMM_pseudocounts(0.7796059561238006, 0.02, 'ABCDE',
                             ['-EABDEBCCC', 'CDABE-CCBC', 'DEAEBC-AEB', 'CCCAD-D--E', 'DAACDECBAE', 'E-CAEEEAAA',
                              '-EBABB-EAB', 'DCD-AD-CAD', '-BCBCAB-CD', 'EE-DDDDDAD', 'D-EEB-ADAD', 'CAECA-EEED',
                              'BECE-CBBEA', 'BDDADDCEBE', 'ABDC-BABB-', 'EBDDB---DC', 'BEBBE-EACE', 'BEBCDADB-C',
                              'EEECEDEDEB', 'ADCEDD-EDE', 'CDECCCB-BC', 'BAAACBECCE', 'D-CD-ECDDE', 'E-BEAEACCA',
                              'DABDBABDDE', 'B-ABECB-DD', 'ADCC-EAC-B', 'EAA-CDCBCC', 'CDAD-DACBC', 'BCCBDEEA-A',
                              'EEDECCBA-B', 'AC-C-EC--C', 'EDCE-EEB-B', 'BC--C-CCAD', 'DB-E-ACCA-', 'CCCDEAAC-E',
                              'ACBDBBCEEA', 'CDABB-BADB', 'BDB-DADDED', 'CBAABD-EEE'])
