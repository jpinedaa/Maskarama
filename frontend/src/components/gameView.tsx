/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-return */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import React, { useEffect, useState, useRef, useMemo } from 'react';
import { useAtom } from 'jotai';
import { useApi } from '~/gameLogic/apiContext';
import {
  simulationStartedAtom, currentEnvironmentAtom, perspectiveAtom,
  environmentsAtom, entitiesAtom, itemsAtom, currentRoomAtom,
  currentCharacterAtom, gameStartedAtom,
  characters,
  rooms,
  currentCharsInRoomAtom
} from '~/gameLogic/gameStateManager';
import ProgressBar from '~/components/progressBar';
import Image from 'next/image';
import MainBackground from './shared/mainBackground';
import useViewportSize from '~/utils/getViewportDimensions';
type GamePhase = 'initial' | 'awaitingInput' | 'processingInput' | 'nextTurn';
const GameView: React.FC = () => {
  // State declarations
  const [displayedText, setDisplayedText] = useState<string>('');
  const [playerInput, setPlayerInput] = useState<string>('');
  const [feedbackMessage, setFeedbackMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [gamePhase, setGamePhase] = useState<'initial' | 'awaitingInput' | 'processingInput' | 'nextTurn'>('initial');

  // Atom declarations
  const [simulationStarted, setSimulationStarted] = useAtom(simulationStartedAtom);
  const [currentEnvironment, setCurrentEnvironment] = useAtom(currentEnvironmentAtom);
  const [perspective, setPerspective] = useAtom(perspectiveAtom);
  const [environments, setEnvironments] = useAtom(environmentsAtom);
  const [entities, setEntities] = useAtom(entitiesAtom);
  const [currentRoom, setCurrentRoom] = useAtom(currentRoomAtom);
  const [currentChar, setCurrentChar] = useAtom(currentCharacterAtom);
  const [items, setItems] = useAtom(itemsAtom);
  const [gameStarted, setGameStarted] = useAtom(gameStartedAtom);
  const [currentCharsInRoom, setCurrentCharsInRoom] = useAtom(currentCharsInRoomAtom);
  const apiService = useApi();
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!simulationStarted) {
      void initializeGame();
    }
  }, [simulationStarted]);

  const initializeGame = async () => {
    try {
      const status = await apiService.getStatus();
      setCurrentEnvironment(status.currentEnvironment ?? null);
      setPerspective(status.perspective ?? null);
      
      await updateGameState();
      
    } catch (error) {
      console.error("Failed to initialize game:", error);
      setDisplayedText("Failed to initialize game. Please try again later.");
    }
  };

  const updateGameState = async () => {
    console.log('updateGameState');
    
    setIsLoading(true);
    try {
      const [envs, ents] = await Promise.all([
        apiService.getEnvironments(),
        apiService.getEntities(),
      ]);
      setEnvironments(envs);
      setEntities(ents);
      updateItems(ents);
      updateCurrentRoom();
      updateCurrentCharacter();
      updateCharsInRoom(ents, envs);  // Pass both ents and envs
    } catch (error) {
      console.error("Failed to update game state:", error);
    } finally {
      setIsLoading(false);
    }
  };
  const updateCharsInRoom = (ents: Record<string, any>, envs: Record<string, any>) => {
    console.log('updateCharsInRoom - ents', ents, 'envs', envs);
    
    // Create a Set of character IDs for faster lookup
    const characterIds = new Set(characters.map(char => char.id));
    
    // Get the current room from envs using currentEnvironment
    const curRoom = envs[currentEnvironment];
    
    if (curRoom && curRoom.entities) {
      // Filter entities in the room that are characters
      const curCharsInRoom = curRoom.entities
        .filter((entityId: string) => characterIds.has(entityId))
        .map((entityId: string) => {
          const character = characters.find(char => char.id === entityId);
          const entityData = ents[entityId];
          return {
            id: entityId,
            name: character?.name ?? '',
            portrait: character?.portrait ?? '',
            state: entityData?.state ?? '',
            // Include other relevant data from entityData if needed
          };
        });
      
      setCurrentCharsInRoom(curCharsInRoom);
      console.log('Updated currentCharsInRoom:', curCharsInRoom);
    } else {
      setCurrentCharsInRoom([]);
      console.log('Set currentCharsInRoom to empty array');
    }
  };
  const updateItems = (ents: Record<string, any>) => {
    console.log('updateItems');
    
    const newItems = Object.entries(ents)
      .filter(([_, entityData]) => entityData.perception === null)
      .map(([entityId, entityData]) => ({
        id: entityId.slice(0, -2),
        isItem: true,
        ...entityData
      }));
    setItems(newItems);
  };

  const updateCurrentRoom = () => {
    if (currentEnvironment) {
      console.log('currentEnvironment', currentEnvironment);
      
      const roomEntity = rooms.find(r => r.id === currentEnvironment);
      setCurrentRoom(roomEntity);
    }
  };

  const updateCurrentCharacter = () => {
    if (perspective) {
      const charEntity = characters.find(c => c.id === perspective);
      setCurrentChar(charEntity);
    }
  };

  const startSimulation = async () => {
    console.log('startSimulation');
    
    setIsLoading(true);
    try {
      console.log('startSimulation', simulationStarted);
      
      const response = await apiService.startSimulation(1);
      const narrationText = response.split("Simulation completed after")[0].trim();
      setDisplayedText(narrationText);
      setSimulationStarted(true);
      setGameStarted(true);
      setGamePhase('awaitingInput');
      await updateGameState();
    } catch (error) {
      console.error("Failed to start simulation:", error);
      setDisplayedText("Failed to start the game. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const initializeSimulation = async () => {
    console.log('initializeSimulation');

    setIsLoading(true);
    try {
      console.log('initializeSimulation', simulationStarted);

      const response = await apiService.getNarration();
      // Narration text is a list of strings, join them with newline
      console.log('here')
      console.log(response)
      const narrationText = response.join('\n');
      setDisplayedText(narrationText);
      setSimulationStarted(true);
      setGameStarted(true);
      setGamePhase('awaitingInput');
      await updateGameState();
    } catch (error) {
      console.error("Failed to initialize simulation:", error);
      setDisplayedText("Failed to initialize the game. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayerInput = async () => {
    if (!playerInput.trim()) {
      setFeedbackMessage("Please enter a valid input.");
      return;
    }
    setIsLoading(true);
    setGamePhase('processingInput');
    try {
      const result = await apiService.submitPlayerInput(playerInput);
      setFeedbackMessage(result.feedback);
      setPlayerInput('');
      if (result.approved) {
        setGamePhase('nextTurn');
      } else {
        setGamePhase('awaitingInput');
      }
    } catch (error) {
      console.error("Failed to submit player input:", error);
      setFeedbackMessage("Failed to process your input. Please try again.");
      setGamePhase('awaitingInput');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNextTurn = async () => {
    setFeedbackMessage('');
    await startSimulation();
  };

  const scrollToBottom = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  };
  const { width } = useViewportSize();
  const backgroundStyle = useMemo(() => {
    const isWideScreen = width < 768;

    return {
      backgroundImage: isWideScreen
        ? "url('/webp/desktopbg.webp')"
        : "url('/webp/bgmobile.webp')",
      backgroundSize: 'cover' , // Adjust as needed
      backgroundPosition: 'center',
      backgroundRepeat: 'repeat-x' ,
    };
  }, [width]);

  if (!simulationStarted) {
    return (
      <div className='flex items-center justify-center h-screen w-full' style={backgroundStyle}>
        <div className='relative flex flex-row justify-center items-center -top-20'>
          <div className='relative w-full min-w-[400px] md:min-w-[600px] h-[200px]'>
            <Image src={'/svg/bwlogo.svg'} alt='logo' fill/>
          </div>
        </div>
        <button 
          onClick={initializeSimulation}
          disabled={isLoading}
          className="absolute inset-x-auto"
        >
          <div className='relative w-[200px] h-[100px] top-20 md:top-28'>
            <Image src={'/svg/playButton.svg'} alt='play' fill/>
          </div>
          
        </button>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <span className="loading loading-spinner loading-lg text-white"></span>
          </div>
        )}
      </div>
    );
  }
  const getProgressPhase = (phase: GamePhase): number => {
    switch (phase) {
      case 'initial': return 0;
      case 'awaitingInput': return 1;
      case 'processingInput': return 2;
      case 'nextTurn': return 3;
      default: return 0;
    }
  };
  return (
    <div className='md:mt-[8vh] flex flex-row w-full h-full md:h-[calc(70vh)] max-h-[calc(92vh)] max-w-[1500px] mx-auto'>
      
      <div className='relative flex flex-col items-center justify-center w-full'>
        <MainBackground />
      <div className='relative flex flex-row justify-center w-full max-w-[1400px] p-4 md:p-8 h-full '>
          <div className=' flex flex-col md:justify-start items-center w-full h-full'>
            <div className=' bg-transparent w-full h-full z-0 flex flex-col justify-start md:flex-row md:justify-center gap-4 items-center'>
              <div className='relative w-full h-1/2 md:h-full max-w-1/2'>
                <Image src={currentRoom?.roomImage ? currentRoom?.roomImage : '/webp/rooms/gardensDemeter01.webp'} alt='bg' fill className='object-cover h-full w-full z-10' />  
              </div>
              <div className='w-full max-w-1/2 h-1/2 md:h-full flex flex-col justify-center bg-transparent text-center md:text-lg'>
                <div ref={scrollContainerRef} className="scroll-content h-2/3 bg-transparent overflow-y-auto">
                  <div className='min-w-full h-2/3 px-4 text-white whitespace-pre-wrap'>
                    <p>{displayedText}</p>
                    {feedbackMessage && (
                      <p className="mt-4 text-yellow-300">{feedbackMessage}</p>
                    )}
                  </div>
                </div>
                <textarea 
                  value={playerInput}
                  onChange={(e) => setPlayerInput(e.target.value)}
                  disabled={isLoading || gamePhase !== 'awaitingInput'}
                  className="w-[90%] h-1/3 my-2 mx-auto bg-[#352623] shadow-xl text-white"
                />
                <button
                  onClick={gamePhase === 'nextTurn' ? handleNextTurn : handlePlayerInput}
                  disabled={isLoading || (gamePhase === 'awaitingInput' && !playerInput.trim())}
                  className="mt-2 mx-auto px-4 py-2 bg-[#F5EDD6] text-bistre rounded w-[90%]"
                >
                  {gamePhase === 'processingInput' ? 'Processing...' : 
                   gamePhase === 'nextTurn' ? 'Next Turn' : 'Submit'}
                </button>
              </div>
            </div>
          </div>
          <div className="ml-8 w-6 h-full flex justify-center items-center">
            <ProgressBar currentPhase={getProgressPhase(gamePhase)} totalPhases={4} />
          </div>
        </div>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-60">
            <span className="loading loading-spinner loading-lg text-white"></span>
          </div>
        )}
      </div>
    </div>
  );
};

export default GameView;