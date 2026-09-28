from backend.dao.etoro_dao import EtoroDAO
from backend.schemas.data_schemas import EtoroDeposits, EtoroDeposit

#deposits = EtoroDAO.query_deposits()
#print(f"deposits: {deposits}")
'''
deposits = EtoroDeposits([
                            EtoroDeposit(amount=200, currency='USD', deposited_at='01-03-2025'),
                            EtoroDeposit(amount=100, currency='USD', deposited_at='31-03-2025'),
                            EtoroDeposit(amount=160, currency='USD', deposited_at='23-05-2025'),
                            EtoroDeposit(amount=150, currency='USD', deposited_at='09-06-2025'),
                            EtoroDeposit(amount=50, currency='USD', deposited_at='11-06-2025'),
                            EtoroDeposit(amount=250, currency='USD', deposited_at='04-08-2025'),
                            EtoroDeposit(amount=250, currency='USD', deposited_at='31-08-2025'),
                            EtoroDeposit(amount=250, currency='USD', deposited_at='26-09-2025'),
                            EtoroDeposit(amount=200, currency='USD', deposited_at='29-10-2025'),
                            EtoroDeposit(amount=200, currency='USD', deposited_at='02-12-2025'),
                            EtoroDeposit(amount=250, currency='USD', deposited_at='02-01-2026'),
                            EtoroDeposit(amount=250, currency='USD', deposited_at='30-01-2026'),
                            EtoroDeposit(amount=200, currency='USD', deposited_at='03-03-2026'),
                            EtoroDeposit(amount=200, currency='USD', deposited_at='10-04-2026'),
                            EtoroDeposit(amount=200, currency='USD', deposited_at='26-05-2025'),
                            EtoroDeposit(amount=311, currency='USD', deposited_at='22-06-2026'),
                            EtoroDeposit(amount=339, currency='USD', deposited_at='15-07-2026'),
                            EtoroDeposit(amount=400, currency='USD', deposited_at='05-08-2026')
                            ])
EtoroDAO.insert_deposits(deposits)

'''

deposits = EtoroDAO.query_deposits()
print(f"deposits: {deposits}")

total_deposits = EtoroDAO.get_total_deposits()
print(f"Total deposits: {total_deposits}")
