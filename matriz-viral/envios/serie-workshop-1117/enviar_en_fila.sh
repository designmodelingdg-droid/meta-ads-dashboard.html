#!/bin/bash
# Envía cargas una por una: espera cola libre, despacha, espera fin, imprime resultado.
R=designmodelingdg-droid/dma-sales-assistant; W=repos/$R/actions/workflows/enviar-grupo.yml
for f in "$@"; do
  until [ "$(gh api "$W/runs?per_page=6" --jq '[.workflow_runs[]|select(.status!="completed")]|length')" = 0 ]; do sleep 8; done
  t0=$(date -u +%FT%TZ); gh api -X POST $W/dispatches --input "$f" || { echo "FALLO despacho $f"; continue; }
  until id=$(gh api "$W/runs?per_page=4&created=>=$t0" --jq '.workflow_runs[-1].id // empty') && [ -n "$id" ]; do sleep 4; done
  until [ "$(gh api repos/$R/actions/runs/$id --jq .status)" = completed ]; do sleep 8; done
  echo "$f · run $id · $(gh api repos/$R/actions/runs/$id --jq .conclusion) · $(gh run view $id -R $R --log 2>/dev/null | sed 's/^.*Z //' | grep -E 'Enviado|rror|enviado a' | head -2 | tr '\n' ' ' | cut -c1-200)"
done
