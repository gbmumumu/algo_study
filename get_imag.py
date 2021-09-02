#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "gbmumumu"

"""
Extract the pictures from excel and then name them in ./images/*
how to use: python get_image.py -f ${*.xlsx} -c ${index of picture} -lb ${index of name}
for example python get_imag.py -f .\123.xlsx -c 0 -lb 1
"""
from pathlib import Path
from collections import OrderedDict
from tqdm import tqdm
import re
import click
import shutil
import zipfile
import pandas
from xml.dom.minidom import parse

LOCAL = Path("./data")


class XlsxImag:
    def __init__(self, xsl):
        self.xsl = Path(xsl)
        self._zip = self.xsl.with_suffix(".zip")
        self.zip = self.init()

    def get_data(self, sheet_name=0):
        return pandas.read_excel(self.xsl, sheet_name).values

    def init(self):
        LOCAL.mkdir(exist_ok=True)
        zips = LOCAL / self._zip.name
        shutil.copy(str(self.xsl), str(zips))
        return zips

    def unzip(self):
        try:
            print(f"Extract files to {self.zip.parent.absolute()}...")
            zipfile.ZipFile(self.zip).extractall(str(self.zip.parent))
        except Exception as e:
            raise IOError from e
        else:
            print("unzip done!")
        return

    def get_relationship(self, image_idx=0, label_idx=1):
        cell_images = LOCAL / "xl" / "_rels" / "cellimages.xml.rels"
        dom_tree = parse(str(cell_images))
        root = dom_tree.documentElement
        print(f"reading {root.nodeName}...")
        results = OrderedDict()
        for image in root.getElementsByTagName("Relationship"):
            results[image.getAttribute("Id")] = image.getAttribute("Target")
        rid_with_name = LOCAL / "xl" / "cellimages.xml"
        rid_name_tree = parse(str(rid_with_name))
        rid_name_root = rid_name_tree.documentElement
        print(f"reading {rid_name_root.nodeName}...")
        rid_name_results = OrderedDict()
        for idx, _image in enumerate(rid_name_root.getElementsByTagName("xdr:cNvPr")):
            rid_name_results[_image.getAttribute("name")] = f"rId{idx + 1}"
        data = self.get_data()
        image_name, image_label = data[:, image_idx], data[:, label_idx]

        def clean_name(name):
            rgx = re.compile(r".*=DISPIMG\(\"(ID_.*)\",\d+\).*")
            return rgx.findall(name)[0]
        # for _image in _root.getElementsByTagName("a:blip"):
        #    print(_image.getAttribute("r:embed"))

        clean_image_names = list(map(clean_name, image_name))
        ship = OrderedDict()
        for index, item in enumerate(clean_image_names):
            ima = results.get(rid_name_results.get(item))
            ship[Path(ima).name] = image_label[index]
        return ship

    def get_images(self, image_idx=0, label_idx=1, out=Path("./images")):
        out.mkdir(exist_ok=True)
        images = self.zip.parent / "xl" / "media"
        if not images.exists():
            print("unknown reason, \'media\' do not exists!")
            exit(1)
        rel = self.get_relationship(image_idx, label_idx)
        for item in tqdm(images.rglob('*')):
            name = rel.get(item.name) + item.suffix
            shutil.copy(str(item), str(out / name))
        print(f"all images saved in {out}, please check!")


@click.command()
@click.option("-f", help="input excel filepath")
@click.option("-c", help="image index", default=0)
@click.option("-lb", help="label index", default=1)
def main(f, c, lb):
    xlsx = XlsxImag(f)
    xlsx.unzip()
    xlsx.get_images(image_idx=c, label_idx=lb)


if __name__ == "__main__":
    main()
