import React from "react";
import { Composition } from "remotion";
import { Motion, TOTAL } from "./Motion";

export const RemotionRoot: React.FC = () => (
  <Composition id="Motion" component={Motion} durationInFrames={Math.round(TOTAL * 30)} fps={30} width={1080} height={1920} />
);
