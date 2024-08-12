import Image from 'next/image';
import RoomSelector from '../roomSelector';
import useViewportSize from '~/utils/getViewportDimensions';
import { useEffect, useState } from 'react';



interface DotPosition {
  x: number;
  y: number;
  roomName: string;
  active: boolean;
  activeColor: string;
  inactiveColor: string;
}

const roomDots: DotPosition[] = [
  { x: 150, y: 170, roomName: 'throneRoom01', active: true, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 150, y: 35, roomName: 'libraryOfAthena', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 265, y: 165, roomName: 'bathHouseAphrodite', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 245, y: 80, roomName: 'heartHestia', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 60, y: 80, roomName: 'forgeOfHephaestus', active: true, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 150, y: 295, roomName: 'gardensDemeter', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 60, y: 290, roomName: 'huntingGroundsArtemis', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 60, y: 180, roomName: 'armoryAres', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 265, y: 265, roomName: 'hermesQuarters', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
];

const roomDotsLarge: DotPosition[] = [
  { x: 315, y: 270, roomName: 'throneRoom01', active: true, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 312, y: 65, roomName: 'libraryOfAthena', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 535, y: 292, roomName: 'bathHouseAphrodite', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 490, y: 120, roomName: 'heartHestia', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 130, y: 110, roomName: 'forgeOfHephaestus', active: true, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 313, y: 538, roomName: 'gardensDemeter', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 110, y: 490, roomName: 'huntingGroundsArtemis', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 140, y: 310, roomName: 'armoryAres', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
  { x: 535, y: 470, roomName: 'hermesQuarters', active: false, activeColor: '#00FF00', inactiveColor: '#FF0000' },
];

interface mapPropsInterface {
    activeRoom: string;
}

const Map: React.FC<mapPropsInterface> = ({ activeRoom }) => {
  const [isLargeMap, setIsLargeMap] = useState<boolean>(false);
  const {width} = useViewportSize();
  const usedDots = isLargeMap ? roomDotsLarge : roomDots;
  useEffect(() => {
    if (width < 768) {
      setIsLargeMap(false);
    } else {
      setIsLargeMap(true);
    }
  }, [width]);
  console.log(activeRoom);
  
  return (
    <div className='relative z-20'>
      <div className='relative w-[220px] md:w-[650px] h-[150px] md:h-[520px] z-20'>
        {usedDots.map((dot) => (
          <span
          key={dot.roomName}
          className={`rounded-full z-30 absolute w-4 h-4 ${
            dot.roomName === activeRoom ? 'bg-opacity-100' : 'bg-opacity-20'
          }`}
          style={{
            top: `${dot.y}px`,
            left: `${dot.x}px`,
            backgroundColor: dot.roomName === activeRoom ? dot.activeColor : dot.inactiveColor,
          }}
        ></span>
        ))}
        <div className='relative w-[320px] md:w-[650px] h-[350px] md:h-[600px] z-20 border-8 border-parchment'>
          <Image src='/webp/map.webp' className='object-cover ' fill alt='map' />
        </div>
        
      </div>
    </div>
  );
};

export default Map;