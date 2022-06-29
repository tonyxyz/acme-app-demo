
from jwkest.jwt import JWT
def decode_tokens(strng):
  jwt = JWT()
  jwt.unpack(strng)
  print("decoded token:")
  print(jwt.payload())

token = 'eyJraWQiOiJBNmhpc0pQamVxUkplWXlTRHFaMHFBRzlVWkQrUkFmUjFhQ1dQZERjZHZvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2ODkxMGJjNS02ZGVlLTQwZWQtYjRlMy1iMDE3MDVhZTgzMjMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0yLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMl9pZWw5S1dad2YiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI2aHIycnRjdmlzaGs5Y3BnNzZkbW42cDlvNCIsImV2ZW50X2lkIjoiNmMwODQ3MDUtZTgyMy00N2NiLTk2MDMtNTliMGEzNjI2M2RkIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiBwaG9uZSBvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF1dGhfdGltZSI6MTY1MzM5NjU1MSwiZXhwIjoxNjUzNDAwMTUxLCJpYXQiOjE2NTMzOTY1NTEsImp0aSI6IjI2M2IxNTQzLTk2NzEtNDMyYS05ZTExLWI0OTAzNzU4OTE3MyIsInVzZXJuYW1lIjoidG9ueWdyZWVuQHRlY2hpZS5jb20ifQ.ZOZ7_rXd2cGedEBuPrhVQepWH5PpfUUldqTJFd_tAiX7ezhsjXEz9hmQdn71fcfsOB_U1X1ctIpAQ1WXJaYJHOulOtpS03O0e10WxtG66aGaEDS83pyhGqUuXW07avEUlu9lf0-9pYkJcj-NTOImP6XHXdQb8YI8Sd8PB4gr4W7tiK45Dy93D7LaSfInXT-Js9KZrer9HYPg6XB22ofaEQEIuDppF_lnRu4GYRGvienWBDMFPSpJ9-oOBxCwJghpiNQgm63ondzRyNtUw7eclxAw5CigCtGXxaUaBhDesD5EqcMDjPaOCi6BaXINpX4KgWsw5fl5-0WT44UmurEyEw'
decode_tokens(token)