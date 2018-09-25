# from domain.Employer import Employer
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Sector(Base):
    __tablename__ = 'sector'
    id = Column('sector_id', Integer, primary_key=True)
    name = Column('sector_name', String)
    totalSalaryPaid = Column('total_salary_paid', Float)
    totalTaxableBenefits = Column('total_taxable_benefits', Float)
    totalEmployers = Column('total_employers', Integer)
    #employers = relationship("Employer")

    def __init__(self, name):
        self.name = name
        self.totalSalaryPaid = 0.0
        self.totalTaxableBenefits = 0.0
        self.totalEmployers = 0

    def addEmployer(self, salaryPaid, taxableBenefits):
        self.totalSalaryPaid += salaryPaid
        self.totalTaxableBenefits += taxableBenefits
        self.totalEmployers += 1
