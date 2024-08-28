from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UUID, BINARY, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Token(Base):
    __tablename__ = 'token_info'
    id = Column(Integer, primary_key=True)
    jwt_token = Column(Text)
    full_name = Column(String(250))
    inn = Column(String(12))
    mchd_id = Column(String(12))
    expiration_date = Column(DateTime)
    token_type = Column(String(3), unique=True)


class KizStatus(Base):
    __tablename__ = 'kiz_status'
    Id = Column(Integer, primary_key=True)
    db_code = Column(Integer)
    code = Column(String(50))
    description = Column(String(255))


class ProductGroup(Base):
    __tablename__ = 'product_group'
    Id = Column(Integer, primary_key=True)
    group_name = Column(String(255))
    description = Column(String(255))


class EmissionType(Base):
    __tablename__ = 'emission_type'
    Id = Column(String(20), primary_key=True)
    description = Column(String(255))


class PackageType(Base):
    __tablename__ = 'package_type'
    Id = Column(String(15), primary_key=True)
    description = Column(String(255))
    comment_tobaco = Column(String(1000))
    comment_other = Column(String(1000))


class ReportStatus(Base):
    __tablename__ = 'report_status'
    Id = Column(Integer, primary_key=True)
    status_name = Column(String(50))
    description = Column(String(50))


class ReportQuery(Base):
    __tablename__ = 'report_query'
    id = Column(Integer, primary_key=True)
    report_id = Column(UUID)
    report_date = Column(DateTime)
    timeout = Column(Integer)
    report_name = Column(String(50))
    inn = Column(String(15))
    pg_id = Column(Integer, ForeignKey('product_group.Id'))
    status_id = Column(Integer, ForeignKey('report_status.Id'))
    status_date = Column(DateTime)
    available_to_download = Column(String(15))
    download_status = Column(String(15))
    file_id = Column(String(36))
    file_data = Column(BINARY)
    save_to_table = Column(Boolean)
    cis_status = Column(String(50))


class CisStock(Base):
    __tablename__ = 'cis_stock'
    id = Column(Integer, primary_key=True)
    stock_date = Column(DateTime)
    cis = Column(String(200))
    gtin = Column(String(14))
    tnvedeaes = Column(String(15))
    producerinn = Column(String(15))
    ownerinn = Column(String(15))
    prvetdocument = Column(String(36))
    productname = Column(String(250))
    brand = Column(String(100))
    ownername = Column(String(100))
    producername = Column(String(100))
    status = Column(String(50))
    emissiontype = Column(String(50))
    packagetype = Column(String(50))
    productgroup = Column(String(50))
    introduceddate = Column(DateTime)
    applicationdate = Column(DateTime)
    emissiondate = Column(DateTime)
    expirationdate = Column(DateTime)
    productiondate = Column(DateTime)
