import React from "react";
import { Composition, Still } from "remotion";
import { Nav, NavProps, navDuration } from "./Nav";
import { NAVS } from "./navs";
import { Clip, Portada, clipDuration } from "./Clip";
import { CLIPS } from "./clips";
import { frames } from "./reel/base";
import { Zapata, T as TZ } from "./reel/Zapata";
import { Uniones, T as TU } from "./reel/Uniones";
import { IaRevit, T as TI } from "./reel/IaRevit";
import { Origenes, T as TO } from "./reel/Origenes";
import { Combos, T as TC } from "./reel/Combos";
import { Medidas, T as TM } from "./reel/Medidas";

export const Root: React.FC = () => (
  <>
    {Object.entries(NAVS).map(([k, p]) => (
      <Composition key={k} id={`nav-${k}`} component={Nav as React.FC<any>} defaultProps={p as NavProps} durationInFrames={navDuration(p)} fps={30} width={1080} height={1920} />
    ))}
    {Object.keys(CLIPS).map((id) => (
      <React.Fragment key={id}>
        <Composition id={`clip-${id}`} component={Clip as React.FC<any>} defaultProps={{ id }} durationInFrames={clipDuration(id)} fps={30} width={1080} height={1920} />
        <Still id={`portada-${id}`} component={Portada as React.FC<any>} defaultProps={{ id }} width={1080} height={1920} />
      </React.Fragment>
    ))}
    <Composition id="reel-uniones" component={Uniones} durationInFrames={frames(TU)} fps={30} width={1080} height={1920} />
    <Composition id="reel-iarevit" component={IaRevit} durationInFrames={frames(TI)} fps={30} width={1080} height={1920} />
    <Composition id="reel-origenes" component={Origenes} durationInFrames={frames(TO)} fps={30} width={1080} height={1920} />
    <Composition id="reel-combos" component={Combos} durationInFrames={frames(TC)} fps={30} width={1080} height={1920} />
    <Composition id="reel-medidas" component={Medidas} durationInFrames={frames(TM)} fps={30} width={1080} height={1920} />
    <Composition id="reel-zapata" component={Zapata} durationInFrames={frames(TZ)} fps={30} width={1080} height={1920} />
  </>
);
