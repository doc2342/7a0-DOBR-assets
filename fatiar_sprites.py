# -*- coding: utf-8 -*-
"""
fatiar_sprites.py

Corta os spritesheets da Vitrine DO-BR (crests/kits/stadiums) em imagens PNG
individuais por ID_Time, só para os times que existem no Copa 7a0
(times_copa.csv) - o jogo mostra no maximo ~11 times por vez (elenco final),
entao nao faz sentido baixar o spritesheet inteiro (21MB) no navegador.

USO
    python fatiar_sprites.py
"""
import csv
import json
import os

from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_TIMES_7A0 = r"C:\Users\PC\Documents\7a0\times_copa.csv"

SHEETS = [
    ("crests_sprite.png", "crests_sprite.json", "crests"),
    ("kits_sprite.png", "kits_sprite.json", "kits"),
    ("stadiums_sprite.png", "stadiums_sprite.json", "stadiums"),
]


def carregar_ids_7a0():
    with open(CAMINHO_TIMES_7A0, encoding="utf-8-sig") as f:
        return {linha["ID_Time"] for linha in csv.DictReader(f)}


def main():
    ids_7a0 = carregar_ids_7a0()
    print(f"{len(ids_7a0)} times no Copa 7a0.")

    for nome_png, nome_json, pasta_saida in SHEETS:
        caminho_png = os.path.join(PASTA, nome_png)
        caminho_json = os.path.join(PASTA, nome_json)
        with open(caminho_json, encoding="utf-8") as f:
            meta = json.load(f)

        tw, th = meta["tile_w"], meta["tile_h"]
        destino = os.path.join(PASTA, pasta_saida)
        os.makedirs(destino, exist_ok=True)

        sheet = Image.open(caminho_png)
        cortados, pulados = 0, 0
        for tid, pos in meta["items"].items():
            if tid not in ids_7a0:
                pulados += 1
                continue
            x, y = pos["x"], pos["y"]
            tile = sheet.crop((x, y, x + tw, y + th))
            tile.save(os.path.join(destino, f"{tid}.png"), optimize=True)
            cortados += 1
        sheet.close()
        print(f"{pasta_saida}: {cortados} imagem(ns) salva(s), {pulados} fora do Copa 7a0 (ignorado(s)).")


if __name__ == "__main__":
    main()
