https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0102/p000407-mt-m90280-z0028-s0102-aux.json

é o arquivo .imgbu que tem os dados


secao 0101
https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;zn=0028;se=0101/dados-de-urna;e=e545;uf=mt;ufbu=mt;mubu=90280/boletim-de-urna
https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;zn=0028;se=0102/dados-de-urna;e=e545;uf=mt;ufbu=mt;mubu=90280/boletim-de-urna

se=0102

f"https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;zn=0028;se={}/dados-de-urna;e=e545;uf=mt;ufbu=mt;mubu=90280/boletim-de-urna"


download arquivo bu

https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0102/796730456a576562426d514c5a5156452b787462346a6f4a4b427474515a365663302d78765a6f506d4a4d3d/o00407-9028000280102.bu
https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0103/68517279564f374d5943376f436a6b6a6a4d465552573178684c6a624655684445697432354b43375342413d/o00407-9028000280103.bu

o hash p montar o link acima conseguimos pegar do link json file:///Users/willianbarbosa/Downloads/p000407-mt-m90280-z0028-s0102-aux.json
796730456a576562426d514c5a5156452b787462346a6f4a4b427474515a365663302d78765a6f506d4a4d3d

1. acessa o aux.json
    -> parametrizavel? ss com a seção!!! em 2 pontos

2. pego o hashes { hash }!!

3. Monto na url de download do arquivo imgbu:
    https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0101/46454f45666441594232333230556a3768696c374e362b5a68574c35466e5177633555333630796b4b38513d/o00407-9028000280158.imgbu
    parametro na seção e com o hash

4. qual o padrao de nome de arquivo imgbu?
    - padrao inicial com 4 ultimos digitos da secao?

0101
json link: https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0101/p000407-mt-m90280-z0028-s0101-aux.json
json: file:///Users/willianbarbosa/Downloads/p000407-mt-m90280-z0028-s0101-aux.json
hash: 46454f45666441594232333230556a3768696c374e362b5a68574c35466e5177633555333630796b4b38513d
imgbu file name: o00407-902800028XXXX -> o00407-9028000280101
download link: https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0101/46454f45666441594232333230556a3768696c374e362b5a68574c35466e5177633555333630796b4b38513d/o00407-9028000280101.imgbu

0102
json link: https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0102/p000407-mt-m90280-z0028-s0102-aux.json
json: file:///Users/willianbarbosa/Downloads/p000407-mt-m90280-z0028-s0102-aux.json
hash: 796730456a576562426d514c5a5156452b787462346a6f4a4b427474515a365663302d78765a6f506d4a4d3d
imgbu file name: o00407-902800028XXXX -> o00407-9028000280102
download link: https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/mt/90280/0028/0102/796730456a576562426d514c5a5156452b787462346a6f4a4b427474515a365663302d78765a6f506d4a4d3d/o00407-9028000280102.imgbu

PARA FAZER
TO USANDO A https://docs.python.org/3.8/library/urllib.request.html#module-urllib.request
https://stackoverflow.com/questions/1393324/given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-contents-of-the
https://stackoverflow.com/questions/36516183/what-should-i-use-to-open-a-url-instead-of-urlopen-in-urllib3
https://urllib3.readthedocs.io/en/stable/

P LER MEU ARQUIVO DE DOWNLOAD, VER SE EU PARSEIO ELE P CONSEGUIR LER LINHA A LINHA

CONFRESA, MT, ZONA 0028 SECAO 0102