Employee = type("Employee", (object,), dict())

date_parser = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
df = pd.read_csv('./data/spple_5m.csv', parse_dates=['date'], date_parser=date_parser)




