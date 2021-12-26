file = 'C:\\Users\\User\\Desktop\\M2-S3\\RI\\Moteur-de-recherche--main\\Moteur-de-recherche--main\\file.txt'
for line in open(file):
      li=line.strip()
      if not li.startswith("#"):
          print (line.rstrip())