import React, { useState, useCallback, useMemo, useEffect } from 'react';
import { useAtom } from 'jotai';
import { entitiesAtom, environmentsAtom, currentEnvironmentAtom, 
  rooms, Room, Item, Character, items, characters, currentCharacterAtom, 
  currentRoomAtom,
  itemsAtom,
  gameStartedAtom} from '~/gameLogic/gameStateManager';
import Image from 'next/image';
import { Entity, Environment } from '~/types/gameModel';
import { ModalType } from '~/types/modal';
import Modal from './shared/modal';
import { isDyslexic } from '~/utils/fontAtom';
import useViewportSize from '~/utils/getViewportDimensions';
import Map from './shared/Map';
interface FloatingWindowProps {
  mapVisible: boolean;
  title: string;
  items:  Entity[] | Environment[] | string[] | Room[] | Item[] | Character[];
  onClose: () => void;
  isOpen: boolean;
  icon: string;
}

interface ButtonData {
  name: string;
  image: string;
  description: string;
  subImg: string;
}

const buttons: ButtonData[] = [
  {
    name: 'Characters',
    image: '/svg/charactericon.svg',
    description: 'View characters in the current room.',
    subImg: '/webp/charactericon.webp',
  },
  {
    name: 'Items',
    image: '/svg/thingicon.svg',
    description: 'View items in the current room.',
    subImg: '/webp/thingicon.webp',
  },
  {
    name: 'Rooms',
    image: '/svg/roomicon.svg',
    description: 'View all available rooms.',
    subImg: '/webp/roomicon.webp',
  },
  {
    name: 'Settings',
    image: '/svg/settingsicon.svg',
    description: 'Adjust game settings.',
    subImg: '/webp/settingsicon.webp',
  },
  {
    name: 'Map',
    image: '/svg/mapicon.svg',
    description: 'View your current location.',
    subImg: '/webp/mapicon.webp',
  }
  
];
// eslint-disable-next-line react-hooks/rules-of-hooks



const FloatingWindow: React.FC<FloatingWindowProps> = ({ title, items, onClose, isOpen,icon, mapVisible }) => {
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [modalType, setModalType] = useState<ModalType>(ModalType.LOGIN);
  const [isDyslexicAtom, setIsDyslexicAtom] = useAtom(isDyslexic);
 

  const openModal = (type: ModalType) => {
    setModalType(type);
    setIsModalOpen(true);
  };
  const closeModal = () => {
    setIsModalOpen(false);
  };

  const renderItem = (item:Environment | Entity | Item | Character | Room | string ) => {

    if (typeof item === 'string') {
      if(item === 'Enable Dyslexia-friendly Font') {
        return <button className="font-semibold" onClick={() => {
          setIsDyslexicAtom(!isDyslexicAtom);
          
        }}>{item}</button>;
        
      }
      const modalType = item === 'Sign Up' ? ModalType.SIGNUP : item === 'Log In' ? ModalType.LOGIN : ModalType.SETTINGS;
      return <button className="font-semibold" onClick={() => openModal(modalType as ModalType)}>{item}</button>;
    } else if ('portrait' in item) {//character
      return (<div className='flex flex-row items-center justify-start w-full h-full px-4'>
           <div className='relative w-[100px] h-full z-10 bg-transparent border-2 border-parchment overflow-hidden'>
                        <video
                            autoPlay
                            loop
                            muted
                            playsInline
                            className='object-cover object-[95%_20%] w-full h-full'
                        >
                            <source src={item.portrait} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </div>
            <h4 className="font-semibold ml-4">{item.name}</h4>
          </div>)
    } else if ('isItem' in item) { //item
      // console.log('item', item);
      
      return (
      <div className='flex flex-row items-center justify-center'>
        <h4 className="font-semibold">{item.id}</h4>
        <p>{item.description}</p>
      </div>
      )
    } else if ('roomImage' in item) {//room
      return (<div className='flex flex-row items-center justify-start w-full h-full pl-3'>
           <div className='relative w-[100px] h-full z-10 bg-transparent border-2 border-parchment overflow-hidden'>
                <Image src={item.roomImage} alt={item.name} fill className='object-cover' />
              </div>
              <h4 className="font-semibold ml-4 text-sm">{item.name}</h4>
            </div>)
    } else {
      return <p>Unknown item type</p>;
    }
  };
  
  return (
    <div>
      {title === 'Map' && <div className={`fixed z-30 top-[35vh] w-screen -translate-y-1/2 left-0  transition-transform duration-700 ease-in-out
      ${isOpen ? 'translate-x-[0%]' : '-translate-x-[800px] sm:-translate-x-full'}`}>
          <Map activeRoom={'palaceCourt'} />
      </div>}
      {title !== 'Map' && 
      <div className={`fixed z-30 top-[48vh] -translate-y-1/2 left-0 w-[300px] md:w-[450px] h-[80vh] overflow-y-hidden 
      transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
         <div className="absolute inset-0 h-full">
          <div className="relative w-full h-[100vh]">
            <Image
              alt='bg'
              src="/webp/popupmenubackground.webp"
              fill
              className="object-cover object-[95%_50%]"
            />
          </div>
        </div>
        
        <div className="relative z-10 h-full flex flex-col">
          <div className="w-[98%] bg-[#915820] p-3 flex justify-between items-center">
            <Image src={icon} alt='icon' width={25} height={25} />
            <h3 className="font-bold text-white text-xl">{title}</h3>
            <button onClick={onClose} className="text-white hover:text-gray-200">×</button>
          </div>
          <ul className="custom-scrollbar overflow-y-auto overflow-x-hidden flex-grow">
            {items.map((item, index) => (
              <li key={index} className="py-2 flex items-center">
                <div className='flex flex-row items-center justify-center w-full h-[100px]'>
                  {/* eslint-disable-next-line @typescript-eslint/no-unsafe-argument */}
                  {renderItem(item)}
                </div>
              </li>
            ))}
          </ul>
        </div>
        {/* {title === 'Map' && <Map activeRoom={'palaceCourt'} />} */}
        <Modal 
          isOpen={isModalOpen}
          onClose={closeModal}
          type={modalType}
        />
      </div>}
    </div>
   
  );
};

const GameButtons: React.FC = () => {
  const [activeWindow, setActiveWindow] = useState<string | null>(null);
  const [mapVisible, setMapVisible] = useState<boolean>(false);
  const [entities] = useAtom(entitiesAtom);
  const [environments] = useAtom(environmentsAtom);
  const [currentEnvironment] = useAtom(currentEnvironmentAtom);
  const [currentChar, setCurrentChar] = useAtom(currentCharacterAtom);
  const [currentRoom, setCurrentRoom] = useAtom(currentRoomAtom);
  const [items] = useAtom(itemsAtom);
  const {width} = useViewportSize();
  const [gameStarted] = useAtom(gameStartedAtom);
  
  const sortedCharacters = useMemo(() => {
    if (!currentChar) return characters;
    return [
      ...characters.filter(char => char.name === currentChar?.name),
      ...characters.filter(char => char.name !== currentChar?.name)
    ];
  }, [characters, currentChar]);

  const sortedRooms = useMemo(()=>{
    if(!currentRoom) return rooms;
    return [
      ...rooms.filter(room => room.name === currentRoom?.name),
      ...rooms.filter(room => room.name !== currentRoom?.name)
    ];
  },[rooms,currentRoom])
  useEffect(() => {
    console.log('currentChar', currentChar);
    console.log('sortedCharacters', sortedCharacters);
  }, [currentChar, sortedCharacters]);

  const handleButtonClick = useCallback((windowName: string) => {
    
      setActiveWindow(prev => prev === windowName ? null : windowName);
    
  }, []);

  const getItemsForWindow = useCallback((windowName: string): Entity[] | Environment[] | string[] | Room[] | Item[] | Character[]=> {
    switch (windowName) {
      case 'Characters':
        return Object.values(sortedCharacters);
      case 'Items':
        return Object.values(items); // Implement item retrieval if needed
      case 'Rooms':
        return Object.values(sortedRooms);
      case 'Settings':
        return ['Sign Up', 'Log In','API Key', 'Enable Dyslexia-friendly Font']; // Placeholder settings
      default:
        return [];
    }
  }, [entities, environments, sortedCharacters]);

  return (
    <div className={`relative flex flex-row gap-6  h-[10vh] justify-start items-center pl-10 bg-transparent ${gameStarted ? '' : 'hidden'}`}
    style={
      { width: `${width}px` }
    }>
      <div className='absolute top-0 left-0 z-10 w-full max-w-[100vw] h-full'>
        <div className='relative w-full max-w-[100vw] h-[10vh]'>
          <Image
            src={'/svg/menubg.svg'}
            fill
            className='w-full max-w-[100vw] object-cover'
            alt='bg'
          />
        </div>
      </div>
      {buttons.map((button, index) => (
        // <div key={index} className="w-fit flex justify-center relative z-10 items-center">
          <button key={index}
            className='z-10'
            onClick={() => handleButtonClick(button.name)}
          >
            <Image src={button.image} alt={button.name} width={65} height={65} />
          </button>
        // </div>
      ))}
      {buttons.map((button) => (
        
        <FloatingWindow 
          mapVisible={mapVisible}
          key={button.name}
          title={button.name} 
          items={getItemsForWindow(button.name)}
          onClose={() => setActiveWindow(null)}
          isOpen={activeWindow === button.name}
          icon={button.subImg}
        />
      ))}
    </div>
  );
};

export default React.memo(GameButtons);