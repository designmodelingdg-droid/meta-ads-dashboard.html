import React from "react";
import { Composition, Still } from "remotion";
import { Nav, NavProps, navDuration } from "./Nav";
import { NAVS } from "./navs";
import { Clip, Portada, clipDuration } from "./Clip";
import { CLIPS } from "./clips";

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
  </>
);
