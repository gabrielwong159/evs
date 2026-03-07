from collections import namedtuple

Transaction = namedtuple('Transaction', 'transaction_id,'
                                        'date,'
                                        'amount,'
                                        'offer_id,'
                                        'payment_mode,'
                                        'channel,'
                                        'status')
