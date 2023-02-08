# python -m pwiz -e mysql -u root -P 124 -p 3306 carteira > model.py

from peewee import *

database = MySQLDatabase('carteira', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'port': 3306, 'user': 'root', 'password': '1234'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

# class Ativos(BaseModel):
#     created_at = DateTimeField(null=True)
#     id = BigAutoField()
#     updated_at = DateTimeField(null=True)

#     class Meta:
#         table_name = 'ativos'

# class FailedJobs(BaseModel):
#     connection = TextField()
#     exception = TextField()
#     failed_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
#     id = BigAutoField()
#     payload = TextField()
#     queue = TextField()
#     uuid = CharField(unique=True)

#     class Meta:
#         table_name = 'failed_jobs'

class HistoricPrices(BaseModel):
    average_price = FloatField(null=True)
    close_price = FloatField(null=True)
    company_name = CharField(null=True)
    created_at = DateTimeField(null=True)
    date = DateField(index=True)
    factor = IntegerField(null=True)
    id = BigAutoField()
    isin = CharField(index=True)
    market = CharField(null=True)
    maximum_price = FloatField(null=True)
    minimum_price = FloatField(null=True)
    open_price = FloatField(null=True)
    specification = CharField(null=True)
    ticker = CharField(index=True)
    updated_at = DateTimeField(null=True)
    volume = IntegerField(null=True)

    class Meta:
        table_name = 'historic_prices'
        indexes = (
            (('date', 'ticker', 'isin'), True),
        )

class IncomeStatements(BaseModel):
    cd_conta = CharField(column_name='cd_conta', index=True)
    cd_cvm = IntegerField(column_name='cd_cvm', index=True)
    cnpj_cia = CharField(column_name='cnpj_cia')
    denom_cia = CharField(column_name='denom_cia')
    ds_conta = CharField(column_name='ds_conta')
    dt_fim_exerc = DateField(column_name='dt_fim_exerc')
    dt_ini_exerc = DateField(column_name='dt_ini_exerc')
    dt_refer = DateField(column_name='dt_refer', index=True)
    escala_moeda = CharField(column_name='escala_moeda')
    moeda = CharField(column_name='moeda')
    st_conta_fixa = CharField(column_name='st_conta_fixa')
    vl_conta = FloatField(column_name='vl_conta')
    id = BigAutoField()

    class Meta:
        table_name = 'income_statements'
        indexes = (
            (('dt_refer', 'cd_conta', 'cd_cvm'), True),
        )

# class Migrations(BaseModel):
#     batch = IntegerField()
#     migration = CharField()

#     class Meta:
#         table_name = 'migrations'

# class PasswordResets(BaseModel):
#     created_at = DateTimeField(null=True)
#     email = CharField(primary_key=True)
#     token = CharField()

#     class Meta:
#         table_name = 'password_resets'

# class PersonalAccessTokens(BaseModel):
#     abilities = TextField(null=True)
#     created_at = DateTimeField(null=True)
#     expires_at = DateTimeField(null=True)
#     id = BigAutoField()
#     last_used_at = DateTimeField(null=True)
#     name = CharField()
#     token = CharField(unique=True)
#     tokenable_id = BigIntegerField()
#     tokenable_type = CharField()
#     updated_at = DateTimeField(null=True)

#     class Meta:
#         table_name = 'personal_access_tokens'
#         indexes = (
#             (('tokenable_type', 'tokenable_id'), False),
#         )

# class Users(BaseModel):
#     created_at = DateTimeField(null=True)
#     email = CharField(unique=True)
#     email_verified_at = DateTimeField(null=True)
#     id = BigAutoField()
#     name = CharField()
#     password = CharField()
#     remember_token = CharField(null=True)
#     updated_at = DateTimeField(null=True)

#     class Meta:
#         table_name = 'users'

