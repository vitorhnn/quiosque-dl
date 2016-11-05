#!/usr/bin/env python3

# quiosque-dl: um pequeno script em Python para baixar arquivos em massa do quiosque da UFRRJ.

import sys
import requests as r
from lxml import html
import os
import datetime
from time import mktime

try:
    import config
except FileNotFoundError:
    print("não foi possível ler o arquivo de configuração! saindo...")
    sys.exit(1)


def get_files(cookies):
    files = []

    # grab the files page
    dom = html.fromstring(
        r.get(
            "http://academico.ufrrj.br/quiosque/aluno/quiosque.php?pag=arquivos",
            cookies=cookies
        ).text
    )

    dom.make_links_absolute(base_url="http://academico.ufrrj.br/quiosque/aluno/")

    current_teacher = None
    current_subject = None
    for div in dom.cssselect("#conteudo > form div"):  # do some dumb stuff on the dom
        html_class = div.attrib["class"]

        if html_class == "arq2_prof":
            current_teacher = div.cssselect(".prof_nome")[0].text_content()
        elif html_class == "arq2_disctur":
            code = div.cssselect(".arq_disc_cod")[0].text_content()
            human_name = div.cssselect(".arq_disc_nome")[0].text_content()
            school_class = div.cssselect(".arq_turma")[0].text_content()

            current_subject = "{}: {}, turma {}".format(code, human_name, school_class)
        elif html_class == "arq2_lista":
            node = div.cssselect(".arq2_nome a")[0]
            name = node.text_content()
            url = node.attrib["href"]

            time = datetime.datetime.strptime(div.cssselect(".arq2_info")[0].text_content().strip()[:30],
                                              "Enviado em %d/%m/%Y %H:%M:%S").timetuple()
            time = mktime(time)

            final_filename = "{} - {}/{}".format(current_teacher, current_subject, name)

            files.append({"url": url, "filename": final_filename, "timestamp": time})

    return files


def ensure_dir(fname):
    dir = os.path.dirname(fname)
    if not os.path.exists(dir):
        os.makedirs(dir)


def main():
    # log in
    payload = {
        'edtIdUs': config.username,
        'edtIdSen': config.password,
        'btnIdOk': " Ok "
    }

    res = r.post("http://academico.ufrrj.br/quiosque/aluno/quiosque.php", data=payload)

    # grab our cookies
    cookies = res.cookies

    # skip the socioeconomic survey if it's there
    r.get("http://academico.ufrrj.br/quiosque/aluno/quiosque.php?pag=inicio&pular_questionario", cookies=cookies)

    for file in get_files(cookies):
        ensure_dir(file["filename"])
        if not os.path.exists(file["filename"]):
            print("downloading {}".format(file["filename"]))
            res = r.get(file["url"], stream=True, cookies=cookies)

            if res.status_code == 200:
                with open(file["filename"], "wb") as fp:
                    for chunk in res.iter_content(1024):
                        fp.write(chunk)

                os.utime(file["filename"], (file["timestamp"], file["timestamp"]))


if __name__ == "__main__":
    main()
