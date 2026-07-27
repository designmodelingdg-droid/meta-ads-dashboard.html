import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import {AnimatedTitle} from "../components/text/AnimatedTitle";
import {GradientBackground} from "../components/backgrounds/GradientBackground";
import {GridPattern} from "../components/backgrounds/GridPattern";
import {CallToAction} from "../components/overlays/CallToAction";
import {ProgressBar} from "../components/overlays/ProgressBar";
import {Watermark} from "../components/overlays/Watermark";
import {SafeArea} from "../components/layout/SafeArea";
import {loadGoogleFont} from "../presets/fonts";

// Brandkit DMA (fijo)
const DMA = {
  azul: "#003e5c",
  naranja: "#ca7520",
  navy: "#001e30",
  heading: "'Overpass', sans-serif",
  body: "'Nunito', sans-serif",
};

const Eyebrow: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({fps, frame, config: {damping: 14, stiffness: 130}});
  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const translateY = interpolate(progress, [0, 1], [-24, 0]);

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${translateY}px)`,
        background: `${DMA.naranja}e6`,
        color: "#ffffff",
        fontFamily: DMA.body,
        fontWeight: 800,
        fontSize: 26,
        letterSpacing: 2,
        padding: "12px 32px",
        borderRadius: 999,
        marginBottom: 28,
      }}
    >
      {text}
    </div>
  );
};

const BenefitBeat: React.FC<{icon: string; text: string}> = ({icon, text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const iconProgress = spring({fps, frame, config: {damping: 12, stiffness: 150}});
  const iconScale = interpolate(iconProgress, [0, 1], [0.3, 1]);
  const iconOpacity = interpolate(frame, [0, 12], [0, 1], {extrapolateRight: "clamp"});

  return (
    <AbsoluteFill style={{justifyContent: "center", alignItems: "center"}}>
      <div
        style={{
          width: 150,
          height: 150,
          borderRadius: "50%",
          background: `linear-gradient(135deg, ${DMA.naranja}, ${DMA.naranja}bb)`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 68,
          marginBottom: 44,
          opacity: iconOpacity,
          transform: `scale(${iconScale})`,
          boxShadow: `0 16px 44px ${DMA.naranja}66`,
        }}
      >
        {icon}
      </div>
      <AnimatedTitle
        text={text}
        fontSize={54}
        fontFamily={DMA.heading}
        fontWeight={800}
        color="#ffffff"
        enterAnimation="slideUp"
        exitAnimation="fade"
        enterDuration={18}
        holdDuration={130}
        exitDuration={15}
        maxWidth="82%"
        lineHeight={1.18}
        textShadow="0 4px 20px rgba(0,0,0,0.4)"
      />
    </AbsoluteFill>
  );
};

export const CalculadoraZapatasTikTok: React.FC = () => {
  loadGoogleFont("Overpass", "400;600;700;800;900");
  loadGoogleFont("Nunito", "400;600;700;800");

  return (
    <AbsoluteFill>
      <GradientBackground
        colors={[DMA.navy, DMA.azul]}
        angle={145}
        animateAngle
        animateSpeed={0.12}
      />
      <GridPattern type="dots" spacing={44} size={2} color="rgba(255,255,255,0.08)" animate animateSpeed={0.3} />

      {/* Hook: nombre del producto */}
      <Sequence from={0} durationInFrames={110}>
        <SafeArea>
          <AbsoluteFill style={{justifyContent: "center", alignItems: "center"}}>
            <Eyebrow text="HERRAMIENTA GRATUITA" />
            <AnimatedTitle
              text="Calculadora de Zapatas"
              fontSize={78}
              fontFamily={DMA.heading}
              fontWeight={900}
              color="#ffffff"
              enterAnimation="scale"
              exitAnimation="slideUp"
              enterDuration={18}
              holdDuration={72}
              exitDuration={15}
              textShadow={`0 4px 24px ${DMA.naranja}66`}
              lineHeight={1.1}
            />
            <div style={{height: 24}} />
            <AnimatedTitle
              text="Design Modeling Academy"
              fontSize={32}
              fontFamily={DMA.body}
              fontWeight={600}
              color="rgba(255,255,255,0.75)"
              enterAnimation="fade"
              exitAnimation="fade"
              enterDuration={20}
              holdDuration={70}
              exitDuration={15}
            />
          </AbsoluteFill>
        </SafeArea>
      </Sequence>

      {/* Beneficio 1 */}
      <Sequence from={100} durationInFrames={180}>
        <SafeArea>
          <BenefitBeat icon="⚡" text={"Diseña tu zapata\nen minutos, no en horas"} />
        </SafeArea>
      </Sequence>

      {/* Beneficio 2 */}
      <Sequence from={270} durationInFrames={180}>
        <SafeArea>
          <BenefitBeat icon="✅" text={"Verifica cortante y\npunzonamiento automáticamente"} />
        </SafeArea>
      </Sequence>

      {/* Beneficio 3 */}
      <Sequence from={440} durationInFrames={180}>
        <SafeArea>
          <BenefitBeat icon="📐" text={"Acero de refuerzo\nlisto para dibujar"} />
        </SafeArea>
      </Sequence>

      {/* CTA final */}
      <Sequence from={600} durationInFrames={300}>
        <SafeArea>
          <AbsoluteFill style={{justifyContent: "center", alignItems: "center"}}>
            <AnimatedTitle
              text="Calculadora de Zapatas"
              fontSize={48}
              fontFamily={DMA.heading}
              fontWeight={800}
              color="#ffffff"
              enterAnimation="slideDown"
              exitAnimation="fade"
              enterDuration={18}
              holdDuration={260}
              exitDuration={15}
            />
            <div style={{height: 20}} />
            <AnimatedTitle
              text={"100% gratis · Sin instalar nada"}
              fontSize={30}
              fontFamily={DMA.body}
              fontWeight={600}
              color="rgba(255,255,255,0.8)"
              enterAnimation="fade"
              exitAnimation="fade"
              enterDuration={20}
              holdDuration={255}
              exitDuration={15}
            />
          </AbsoluteFill>
        </SafeArea>
        <CallToAction
          text="Accede gratis"
          subtext="Link en bio"
          backgroundColor={`${DMA.naranja}f2`}
          textColor="#ffffff"
          accentColor="rgba(255,255,255,0.85)"
          fontFamily={DMA.heading}
          position="bottom"
          enterDelay={20}
        />
      </Sequence>

      <ProgressBar color={DMA.naranja} height={4} />
      <Watermark
        text="Design Modeling Academy"
        corner="topRight"
        opacity={0.6}
        fontSize={16}
        color="#ffffff"
        margin={40}
      />
    </AbsoluteFill>
  );
};
