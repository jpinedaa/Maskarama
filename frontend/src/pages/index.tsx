import Head from "next/head";
import GameButtons from '~/components/gameButtons';
import GameView from '../components/gameView';
import { useAtom } from 'jotai';
import { isDyslexic } from '~/utils/fontAtom';
import { Outfit, Lexend } from "next/font/google";
import { useEffect, useMemo } from 'react';
import clsx from 'clsx';
import useViewportSize from '~/utils/getViewportDimensions';
import HeroDisplay from '~/components/shared/HeroDisplay';
import FakeGameView from '~/components/fakeGameView';

const outfitFont = Outfit({ subsets: ["latin"], weight: ["200", "400"] });
const lexendFont = Lexend({ subsets: ["latin"], weight: ["200", "400"] });

export default function Home() {
  const [isDyslexicAtom, setIsDyslexicAtom] = useAtom(isDyslexic);
  const { width } = useViewportSize();
  
  useEffect(() => {
    console.log(isDyslexicAtom);
  }, [isDyslexicAtom]);

  const backgroundStyle = useMemo(() => {
    const isWideScreen = width < 768;
    
    return {
      backgroundImage: isWideScreen 
        ? "url('/svg/mobilebg.svg')"
        : "url('/svg/mosaic.svg')",
      backgroundSize: 'cover' , // Adjust as needed
      backgroundPosition: 'center',
      backgroundRepeat: 'repeat-x' ,
    };
  }, [width]);

  return (
    <>
      <Head>
        <title>Echoes of Creation</title>
        <meta name="description" content="Echoes of Creation" />
        <link rel="icon" href="/svg/browsericonlight.svg" />
      </Head>
      <main 
        className={clsx(
          'flex flex-col items-start justify-between h-[101vh] max-h-[110vh] overflow-hidden',
          isDyslexicAtom ? lexendFont.className : outfitFont.className
        )}
        style={backgroundStyle}
      >
        <GameView />
        <HeroDisplay />
        <GameButtons />
      </main>
    </>
  );
  
}