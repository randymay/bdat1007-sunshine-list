import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud import storage
from google.cloud import datastore
from domain.SectorModule import Sector
from domain.EmployerModule import Employer

def loadData():
    print ('Loading data.')
    # CSV_URL = "https://files.ontario.ca/en-2017-pssd-compendium-20180320-utf8.csv"
    CSV_URL = "en-2017-pssd-compendium-20180320-utf8.csv" 

    df_sunshine_data = pd.read_csv(CSV_URL, dtype='str')

    df_sunshine_data['Salary Paid'] = df_sunshine_data['Salary Paid'].str.replace(',', '')
    df_sunshine_data['Salary Paid'] = df_sunshine_data['Salary Paid'].str.replace('$', '')
    df_sunshine_data['Salary Paid'] = df_sunshine_data['Salary Paid'].astype(float)

    df_sunshine_data['Taxable Benefits'] = df_sunshine_data['Taxable Benefits'].str.replace(',', '')
    df_sunshine_data['Taxable Benefits'] = df_sunshine_data['Taxable Benefits'].str.replace('$', '')
    df_sunshine_data['Taxable Benefits'] = df_sunshine_data['Taxable Benefits'].astype(float)

    # df_employers_by_sector = df_sunshine_data.groupby('Sector').agg({'Employer':'count', 'Salary Paid': 'sum', 'Taxable Benefits': 'sum'})
    df_total_by_employer = df_sunshine_data.groupby(['Sector','Employer']).agg({'Salary Paid': 'sum', 'Taxable Benefits': 'sum'})
    #.sort_values('Employer')

    sector = Sector('Placeholder')
    employer = Employer('Placeholder')

    sector_dict = {}
    employer_dict = {}
    client = datastore.Client()

    sectorCount = 0
    employerCount = 0
    employeeCount = 0

    # Create a connection to the DB
    engine = create_engine('mysql+mysqldb://bdat1007:password@35.196.230.121/sunshine_list')
    # engine = create_engine('mysql+mysqldb://bdat1007:password@35.196.230.121/bdat1007-sunshine-list:us-east1:new-sunshine-db')

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for iter, row in df_total_by_employer.iterrows(): 
            employeeCount += 1

            sectorName = iter[0]
            employerName = iter[1]
            print('Sector: {0} - Employer: {1}'.format(sectorName, employerName))
            sectorName = sectorName.encode('UTF-8').decode('ISO-8859-1')
            employerName = employerName.encode('UTF-8').decode('ISO-8859-1')
            salaryPaid = row[0]
            taxableBenefits = row[1]

            # sector = session.query(Sector).filter(Sector.name == sectorName).options(lazyload('employers')).first()
            sector = session.query(Sector).filter(Sector.name == sectorName).first()
            # print(sector)

            if sector is None:
                sectorCount += 1

                sector = Sector(sectorName)
                session.add(sector)
            
            sector.addEmployer(salaryPaid, taxableBenefits)
            # session.add(sector)
            # session.commit()

            employer = session.query(Employer).filter(Employer.name == employerName).first()
            # print(employer)

            if employer is None:
                employerCount += 1

                employer = Employer(employerName)
                employer.sectorId = sector.id
                session.add(employer)

            employer.addEmployee(salaryPaid, taxableBenefits)

            #session.add(employer)

            #print(sector)

        # commit.  The pending changes above
        # are flushed via flush(), the Transaction
        # is committed, the Connection object closed
        # and discarded, the underlying DBAPI connection
        # returned to the connection pool.
        session.commit()
    except:
        # on rollback, the same closure of state
        # as that of commit proceeds.
        session.rollback()
        raise
    finally:
        # close the Session.  This will expunge any remaining
        # objects as well as reset any existing SessionTransaction
        # state.  Neither of these steps are usually essential.
        # However, if the commit() or rollback() itself experienced
        # an unanticipated internal failure (such as due to a mis-behaved
        # user-defined event handler), .close() will ensure that
        # invalid state is removed.
        session.close()

    print ('%s sectors processed' % sectorCount)
    print ('%s employers processed' % employerCount)
    print ('%s employees processed' % employeeCount)

loadData()