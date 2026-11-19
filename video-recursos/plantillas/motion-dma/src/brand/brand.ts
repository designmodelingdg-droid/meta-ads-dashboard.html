// Copyright (c) 2026 Enrique Rocha (@soyenriquerocha)
// SPDX-License-Identifier: MIT
// id: er-22575577
import { loadFont as loadDisplay } from "@remotion/google-fonts/Anton";
import { loadFont as loadBody } from "@remotion/google-fonts/Overpass";
import raw from "../../brand.json";

// Para cambiar de fuente: elige otra en @remotion/google-fonts, cambia estos
// imports y actualiza brand.json. Ver skills/motion-architect/references/brand.md
const display = loadDisplay("normal", { weights: ["400"], subsets: ["latin"] });
const body = loadBody("normal", { weights: ["400", "600", "800"], subsets: ["latin"] });

export const brand = {
  ...raw,
  fontDisplay: display.fontFamily,
  fontBody: body.fontFamily,
};

export type Brand = typeof brand;
