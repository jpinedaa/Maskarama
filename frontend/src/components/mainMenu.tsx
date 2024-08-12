import { useMemo } from 'react';
import useViewportSize from '~/utils/getViewportDimensions';
import Image from 'next/image';

interface MainMenuProps {
  startSimulation: () => void;
  isLoading: boolean;
}

const MainMenu: React.FC<MainMenuProps> = ({ startSimulation, isLoading }) => {
    const { width } = useViewportSize();
    const backgroundStyle = useMemo(() => {
        const isWideScreen = width < 768;
        return {
          backgroundImage: isWideScreen 
            ? "url('/webp/bgmobile.webp')"
            : "url('/webp/desktopbg.webp')",
          backgroundSize: 'cover' , // Adjust as needed
          backgroundPosition: 'center',
          backgroundRepeat: 'repeat-x' ,
        };
      }, [width]);
      
  return (
    <div className='flex items-center justify-center h-screen w-full'>
        <div className='relative flex flex-row justify-center items-center -top-20'
        >
          <div className='relative w-full min-w-[250px] max-w-[350px] h-[200px]'>
            {/* <Image src={'/svg/browsericonlight.svg'} alt='logo' fill/> */}
            <Image src={'/svg/bwlogo.svg'} alt='logo' fill/>
          </div>
          {/* <h1 className='text-6xl font-bold'>Maskarema</h1> */}
        </div>
        <button
          onClick={startSimulation}
          disabled={isLoading}
          className="absolute inset-x-auto"
        >
          <div className='relative w-[200px] h-[100px] top-20'>
            <Image src={'/svg/playButton.svg'} alt='play' fill/>
          </div>
          
        </button>
      </div>
  );
}

export default MainMenu;