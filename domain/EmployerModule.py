# from domain.Sector import Sector
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

Base = declarative_base()

class Employer (Base):
    __tablename__ = 'employer'
    id = Column('employer_id', Integer, primary_key=True)
    name = Column('employer_name', String)
    totalSalaryPaid = Column('total_salary_paid', Float)
    totalTaxableBenefits = Column('total_taxable_benefits', Float)
    totalEmployees = Column('total_employees', Integer)
    #sectorId = Column('sector_id', Integer, ForeignKey('sector.sector_id'))
    sectorId = Column('sector_id', Integer)

    def __init__(self, name):
        self.name = name
        self.totalSalaryPaid = 0.0
        self.totalTaxableBenefits = 0.0
        self.totalEmployees = 0

    def addEmployee(self, salaryPaid, taxableBenefits):
        self.totalSalaryPaid += salaryPaid
        self.totalTaxableBenefits += taxableBenefits
        self.totalEmployees += 1
