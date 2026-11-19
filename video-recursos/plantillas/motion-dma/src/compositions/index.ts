// Copyright (c) 2026 Enrique Rocha (@soyenriquerocha)
// SPDX-License-Identifier: MIT
// id: er-22575577
import { RutaMaster, RM_DURATION } from "./RutaMaster";
import { RutaCine, RC_DURATION } from "./RutaCine";
import { RutaFusion, RF_DURATION } from "./RutaFusion";
import { Coleccion, COL_DURATION } from "../rutas/Coleccion";
import { Especializaciones, ESP_DURATION } from "../rutas/Especializaciones";
import { Acero, ACERO_DURATION } from "../rutas/Acero";
import { Diplomado, DIPLO_DURATION } from "../rutas/Diplomado";
import { Conexion, CONEXION_DURATION } from "../rutas/Conexion";
import { AdCromo, ADCROMO_DURATION } from "../rutas/AdCromo";

// Registro de composiciones. Cada entrada se publica en los formatos que indiques
// con el id "<id>-<formato>" (p. ej. "RutaAcero-vertical").
// Para agregar un video nuevo: crea src/compositions/MiVideo.tsx y añádelo aquí.
export const compositions = [
  {
    id: "RutaMaster",
    component: RutaMaster,
    durationInFrames: RM_DURATION,
    formats: ["vertical", "landscape"],
  },
  {
    id: "RutaCine",
    component: RutaCine,
    durationInFrames: RC_DURATION,
    formats: ["vertical", "landscape"],
  },
  {
    id: "RutaFusion",
    component: RutaFusion,
    durationInFrames: RF_DURATION,
    formats: ["vertical", "landscape"],
  },
  { id: "RutaColeccion", component: Coleccion, durationInFrames: COL_DURATION, formats: ["vertical", "landscape"] },
  { id: "RutaEspecializaciones", component: Especializaciones, durationInFrames: ESP_DURATION, formats: ["vertical", "landscape"] },
  { id: "RutaAcero", component: Acero, durationInFrames: ACERO_DURATION, formats: ["vertical", "landscape"] },
  { id: "RutaDiplomado", component: Diplomado, durationInFrames: DIPLO_DURATION, formats: ["vertical", "landscape"] },
  { id: "AnatomyConexion", component: Conexion, durationInFrames: CONEXION_DURATION, formats: ["vertical", "landscape"] },
  { id: "AdWorkshopCromo", component: AdCromo, durationInFrames: ADCROMO_DURATION, formats: ["vertical"] },
] as const satisfies ReadonlyArray<{
  id: string;
  component: React.FC;
  durationInFrames: number;
  formats: ReadonlyArray<"landscape" | "vertical" | "square" | "portrait">;
}>;
